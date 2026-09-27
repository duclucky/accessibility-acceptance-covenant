"""Allowlist-only normalization for GenLayer lifecycle evidence."""

from __future__ import annotations

from typing import Any


def normalize_receipt(raw: dict[str, Any]) -> dict[str, Any]:
    data = raw.get("data") if isinstance(raw.get("data"), dict) else {}
    lifecycle = raw.get("lifecycle") if isinstance(raw.get("lifecycle"), dict) else {}
    fees = raw.get("fees") if isinstance(raw.get("fees"), dict) else {}
    return {
        "transaction_hash": raw.get("tx_id") or raw.get("hash") or raw.get("transactionHash"),
        "contract_address": data.get("contract_address") or raw.get("contract_address") or raw.get("recipient"),
        "status": raw.get("statusName") or raw.get("status_name") or lifecycle.get("state"),
        "consensus_result": raw.get("result_name") or raw.get("consensus_result"),
        "execution_result": raw.get("txExecutionResultName") or raw.get("tx_execution_result_name"),
        "fee_deposit": fees.get("deposit") or data.get("fee_value"),
        "user_value": fees.get("userValue") or data.get("user_value"),
    }


def require_finalized_success(receipt: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_receipt(receipt)
    status = str(normalized["status"] or "").upper()
    if "FINALIZED" not in status:
        raise ValueError("transaction is not finalized")
    if normalized["execution_result"] != "FINISHED_WITH_RETURN":
        raise ValueError("transaction execution did not finish with return")
    return normalized
