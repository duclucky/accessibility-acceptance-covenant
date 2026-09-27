"""Resumable Studio-dev deployment with allowlist-only evidence output."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from eth_account import Account
from genlayer_py import create_client
from genlayer_py.chains import studio_devnet

from receipt_parser import require_finalized_success


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "contracts" / "accessibility_acceptance_covenant.py"
EVIDENCE = ROOT / "docs" / "evidence" / "studio-dev" / "deployment.json"


def load_key() -> str:
    for env_path in (ROOT / ".env", ROOT.parent / ".env"):
        if not env_path.exists():
            continue
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" not in line or line.lstrip().startswith("#"):
                continue
            name, value = line.split("=", 1)
            if name.strip() == "STUDIONET_PRIVATE_KEY" and value.strip():
                return value.strip().strip('"').strip("'")
    raise RuntimeError("authorized parent key is unavailable")


def main() -> None:
    code = SOURCE.read_text(encoding="utf-8")
    source_hash = hashlib.sha256(code.encode()).hexdigest()
    account = Account.from_key(load_key())
    client = create_client(chain=studio_devnet, account=account)

    if EVIDENCE.exists():
        prior = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        if prior.get("source_sha256") != source_hash or prior.get("chain_id") != 61997:
            raise RuntimeError("deployment checkpoint fingerprint mismatch")
        tx_hash = prior["transaction_hash"]
    else:
        estimate = client.estimate_transaction_fees()
        tx_hash = client.deploy_contract(code, fees=estimate)
        tx_hash = tx_hash.hex() if hasattr(tx_hash, "hex") else str(tx_hash)

    receipt = client.wait_for_transaction_receipt(
        tx_hash, wait_until="finalized", interval=3000, retries=40, full_transaction=True
    )
    safe = require_finalized_success(dict(receipt))
    lifecycle = client.get_transaction_lifecycle(tx_hash)
    if "FINALIZED" not in str(lifecycle.get("projected_status_name", "")).upper():
        raise RuntimeError("projected lifecycle is not finalized")
    record = {
        "record_type": "deployment",
        "network": "studio-dev",
        "chain_id": 61997,
        "rpc": "https://studio-dev.genlayer.com/api",
        "explorer": "https://explorer-studio-dev.genlayer.com",
        "source_sha256": source_hash,
        "runner": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng",
        **safe,
        "lifecycle": "FINALIZED",
        "explorer_contract_url": f"https://explorer-studio-dev.genlayer.com/address/{safe['contract_address']}",
        "explorer_transaction_url": f"https://explorer-studio-dev.genlayer.com/transactions/{safe['transaction_hash']}",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "transaction_hash": safe["transaction_hash"],
        "contract_address": safe["contract_address"],
        "lifecycle": "FINALIZED",
        "consensus_result": safe["consensus_result"],
        "execution_result": safe["execution_result"],
    }))


if __name__ == "__main__":
    main()
