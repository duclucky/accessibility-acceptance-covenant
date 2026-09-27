from scripts.receipt_parser import normalize_receipt, require_finalized_success


def test_normalizes_raw_studio_shape_without_private_fields():
    result = normalize_receipt({
        "tx_id": "0xabc", "statusName": "FINALIZED", "result_name": "MAJORITY_AGREE",
        "txExecutionResultName": "FINISHED_WITH_RETURN",
        "data": {"contract_address": "0xdef", "fee_value": "100", "user_value": 0},
        "consensus_data": {"validators": [{"node_config": {"secret": "never copy"}}]},
    })
    assert result == {
        "transaction_hash": "0xabc", "contract_address": "0xdef", "status": "FINALIZED",
        "consensus_result": "MAJORITY_AGREE", "execution_result": "FINISHED_WITH_RETURN",
        "fee_deposit": "100", "user_value": 0,
    }


def test_normalizes_projected_shape_and_requires_finality():
    projected = {
        "hash": "0xabc", "recipient": "0xdef", "lifecycle": {"state": "finalized"},
        "consensus_result": "MAJORITY_AGREE", "tx_execution_result_name": "FINISHED_WITH_RETURN",
        "fees": {"deposit": "100", "userValue": "0"},
    }
    assert require_finalized_success(projected)["status"] == "finalized"


def test_rejects_accepted_only_receipt():
    try:
        require_finalized_success({"statusName": "ACCEPTED", "txExecutionResultName": "FINISHED_WITH_RETURN"})
    except ValueError as error:
        assert "not finalized" in str(error)
    else:
        raise AssertionError("accepted-only receipt must not pass")
