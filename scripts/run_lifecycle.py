"""Resumable canonical Studio-dev lifecycle with sanitized checkpoints."""

from __future__ import annotations

import base64
import hashlib
import json
import time
import urllib.request
from pathlib import Path
from typing import Any

from eth_account import Account
from genlayer_py import create_client
from genlayer_py.chains import studio_devnet
from genlayer_py.types import CalldataAddress

from receipt_parser import require_finalized_success


ROOT = Path(__file__).resolve().parents[1]
DEPLOYMENT = json.loads((ROOT / "docs/evidence/studio-dev/deployment.json").read_text())
ADDRESS = DEPLOYMENT["contract_address"]
OUT = ROOT / "docs/evidence/studio-dev/lifecycle.json"
CASE_ID = "aac-demo-20260927-v1"
VENDOR = "0x017d13fe11263159470130ec1f2f96879e8fd40c"
POLICY_URL = "https://www.w3.org/TR/WCAG22/"


def env_values() -> dict[str, str]:
    values: dict[str, str] = {}
    for path in (ROOT / ".env", ROOT.parent / ".env"):
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.lstrip().startswith("#"):
                    key, value = line.split("=", 1)
                    values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def report_url(role: str) -> tuple[str, str]:
    body = json.dumps({
        "evaluator": role,
        "release_id": "release-2026-09-27",
        "samples": ["sample-a", "sample-b"],
        "complete_processes": ["process-a"],
        "criteria": ["criterion-a", "criterion-b"],
        "findings": [],
        "conclusion": "all locked evaluation-record coverage is present and no unresolved finding remains",
    }, separators=(",", ":")).encode()
    encoded = base64.b64encode(body).decode().rstrip("=")
    return "https://httpbin.org/base64/" + encoded, hashlib.sha256(body).hexdigest()


def finalized_write(client, account, method: str, args: list[Any]) -> dict[str, Any]:
    try:
        estimate = client.estimate_transaction_fees_for_write(
            ADDRESS, method, account=account, args=args
        )
    except Exception:
        # Studio's targeted simulation can fail before returning a report for
        # role-specific calls. The generic current-policy quote remains a
        # bounded fee preset; the finalized receipt is still authoritative.
        estimate = client.estimate_transaction_fees()
    tx_hash = client.write_contract(
        ADDRESS, method, account=account, args=args, fees=estimate
    )
    tx_hash = tx_hash.hex() if hasattr(tx_hash, "hex") else str(tx_hash)
    receipt = client.wait_for_transaction_receipt(
        tx_hash, wait_until="finalized", interval=3000, retries=50, full_transaction=True
    )
    safe = require_finalized_success(dict(receipt))
    safe["method"] = method
    return safe


def main() -> None:
    values = env_values()
    buyer = Account.from_key(values["STUDIONET_PRIVATE_KEY"])
    primary = Account.from_key(values["STUDIONET_INTEGRATOR_PRIVATE_KEY"])
    corroborating = Account.from_key(values["STUDIONET_STEWARD_PRIVATE_KEY"])
    client = create_client(chain=studio_devnet, account=buyer)
    checkpoint = json.loads(OUT.read_text()) if OUT.exists() else {"transactions": []}
    transactions: list[dict[str, Any]] = checkpoint["transactions"]

    policy = urllib.request.urlopen(POLICY_URL, timeout=30).read()
    policy_digest = hashlib.sha256(policy).hexdigest()
    primary_url, primary_digest = report_url("primary")
    corroborating_url, corroborating_digest = report_url("corroborating")
    now = int(time.time())

    try:
        case = client.read_contract(ADDRESS, "get_case", args=[CASE_ID])
    except Exception:
        case = None
    if case is None:
        transactions.append(finalized_write(client, buyer, "create_case", [
            CASE_ID, CalldataAddress(VENDOR), CalldataAddress(primary.address),
            CalldataAddress(corroborating.address), "product-a", "release-2026-09-27",
            "wcag22-profile-v1", POLICY_URL, policy_digest, "sample-a|sample-b",
            "process-a", "criterion-a|criterion-b", "finding-a|finding-b",
            now + 3600, now + 7200, now + 10800, now + 14400,
        ]))
        case = client.read_contract(ADDRESS, "get_case", args=[CASE_ID])
    state = case["state"]
    if state == "DRAFT":
        transactions.append(finalized_write(client, buyer, "activate_case", [CASE_ID]))
        state = "ACTIVE"
    if state == "ACTIVE":
        issued_at = int(time.time())
        transactions.append(finalized_write(client, primary, "submit_evaluator_report", [
            CASE_ID, "PRIMARY", primary_url, primary_digest, "primary-v1", issued_at,
        ]))
        state = "EVIDENCE_PENDING"
    if state == "EVIDENCE_PENDING":
        issued_at = int(time.time())
        transactions.append(finalized_write(client, corroborating, "submit_evaluator_report", [
            CASE_ID, "CORROBORATING", corroborating_url, corroborating_digest,
            "corroborating-v1", issued_at,
        ]))
        state = "EVIDENCE_READY"
    if state == "EVIDENCE_READY":
        transactions.append(finalized_write(client, buyer, "adjudicate", [CASE_ID, "adjudication-v1"]))

    case = client.read_contract(ADDRESS, "get_case", args=[CASE_ID])
    verdict = client.read_contract(ADDRESS, "get_verdict", args=[CASE_ID])
    if case["state"] == "ACCEPTED":
        transactions.append(finalized_write(client, buyer, "finalize_procurement_acceptance", [CASE_ID]))
        case = client.read_contract(ADDRESS, "get_case", args=[CASE_ID])
    eligible = client.read_contract(ADDRESS, "is_release_eligible", args=[CASE_ID])
    record = {
        "record_type": "canonical_lifecycle",
        "network": "studio-dev", "chain_id": 61997, "contract_address": ADDRESS,
        "case_id": CASE_ID, "policy_url": POLICY_URL, "policy_sha256": policy_digest,
        "policy_byte_length": len(policy), "report_transport": "httpbin exact base64 endpoint",
        "transactions": transactions,
        "canonical_case": case, "canonical_verdict": verdict,
        "canonical_consequence": {"release_eligible": eligible},
        "limitations": [
            "Demo reports are synthetic exact-byte fixtures, not evidence of real procurement adoption.",
            "Transaction identities authenticate fixture submitters; they do not prove evaluator competence."
        ],
    }
    OUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "state": case["state"], "verdict": verdict["verdict"],
        "release_eligible": eligible, "finalized_transactions": len(transactions),
    }))


if __name__ == "__main__":
    main()
