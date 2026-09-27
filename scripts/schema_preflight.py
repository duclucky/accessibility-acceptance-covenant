from pathlib import Path

from genlayer_py import create_client
from genlayer_py.chains import studio_devnet


SOURCE = Path("contracts/accessibility_acceptance_covenant.py")
EXPECTED_WRITES = {
    "create_case", "activate_case", "submit_vendor_context", "submit_evaluator_report",
    "adjudicate", "retry_unverifiable", "submit_cure", "submit_cure_addendum",
    "readjudicate_cure", "finalize_procurement_acceptance", "close_expired",
}


def main() -> None:
    code = SOURCE.read_text(encoding="utf-8")
    if not code.startswith('# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }'):
        raise SystemExit("runner header mismatch")
    schema = create_client(chain=studio_devnet).get_contract_schema_for_code(code)
    methods = schema.get("methods", {})
    writes = {name for name, value in methods.items() if not value.get("readonly")}
    if writes != EXPECTED_WRITES:
        raise SystemExit(f"write schema mismatch: {sorted(writes)}")
    print(f"studio-dev schema ok: {len(methods)} methods, {len(writes)} writes, chain 61997")


if __name__ == "__main__":
    main()
