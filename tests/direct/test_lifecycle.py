from __future__ import annotations

import hashlib
import json


CONTRACT = "contracts/accessibility_acceptance_covenant.py"
POLICY_DIGEST = "a" * 64


def create_case(contract, buyer, vendor, primary, corroborating, policy_digest=POLICY_DIGEST) -> None:
    import genlayer as gl

    contract.create_case(
        "case-1",
        gl.Address(vendor),
        gl.Address(primary),
        gl.Address(corroborating),
        "product-1",
        "release-1",
        "profile-v1",
        "https://www.w3.org/TR/2025/REC-WCAG22-20251212/",
        policy_digest,
        "sample-a|sample-b",
        "process-a",
        "criterion-a|criterion-b",
        "finding-a|finding-b",
        2_000_000_100,
        2_000_000_200,
        2_000_000_300,
        2_000_000_400,
    )


def test_create_case_locks_structured_profile_and_rejects_duplicate(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    direct_charlie,
    direct_accounts,
):
    direct_vm.warp("2033-05-18T03:33:20Z")  # 2_000_000_000
    direct_vm.sender = direct_alice
    contract = direct_deploy(CONTRACT)

    create_case(
        contract,
        direct_alice,
        direct_bob,
        direct_charlie,
        direct_accounts[3],
    )

    case = contract.get_case("case-1")
    profile = contract.get_profile("case-1")
    assert case["state"] == "DRAFT"
    import genlayer as gl

    assert case["buyer"] == str(gl.Address(direct_alice))
    assert case["vendor"] == str(gl.Address(direct_bob))
    assert profile["release_id"] == "release-1"
    assert profile["sample_ids"] == "sample-a|sample-b"
    assert profile["criterion_ids"] == "criterion-a|criterion-b"
    assert contract.get_case_count() == 1
    assert contract.is_release_eligible("case-1") is False

    with direct_vm.expect_revert("Case already exists"):
        create_case(
            contract,
            direct_alice,
            direct_bob,
            direct_charlie,
            direct_accounts[3],
        )


def prepared_case(direct_vm, direct_deploy, buyer, vendor, primary, corroborating):
    direct_vm.warp("2033-05-18T03:33:20Z")
    direct_vm.sender = buyer
    contract = direct_deploy(CONTRACT)
    create_case(contract, buyer, vendor, primary, corroborating)
    contract.activate_case("case-1")
    return contract


def test_activation_and_report_roles_are_enforced(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    direct_charlie,
    direct_accounts,
):
    corroborating = direct_accounts[3]
    contract = prepared_case(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, corroborating
    )
    assert contract.get_case("case-1")["state"] == "ACTIVE"

    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("Evaluator caller mismatch"):
        contract.submit_evaluator_report(
            "case-1", "PRIMARY", "https://evidence.example/primary.json", "b" * 64,
            "nonce-p", 2_000_000_000,
        )

    direct_vm.sender = direct_charlie
    contract.submit_evaluator_report(
        "case-1", "PRIMARY", "https://evidence.example/primary.json", "b" * 64,
        "nonce-p", 2_000_000_000,
    )
    assert contract.get_case("case-1")["state"] == "EVIDENCE_PENDING"

    with direct_vm.expect_revert("Report already submitted"):
        contract.submit_evaluator_report(
            "case-1", "PRIMARY", "https://evidence.example/other.json", "c" * 64,
            "nonce-p2", 2_000_000_000,
        )

    direct_vm.sender = corroborating
    contract.submit_evaluator_report(
        "case-1", "CORROBORATING", "https://evidence.example/corroborating.json",
        "c" * 64, "nonce-c", 2_000_000_000,
    )
    evidence = contract.get_evidence("case-1")
    assert contract.get_case("case-1")["state"] == "EVIDENCE_READY"
    assert evidence["primary_nonce"] == "nonce-p"
    assert evidence["corroborating_nonce"] == "nonce-c"


def test_finalize_requires_buyer_and_accepted_state(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    direct_charlie,
    direct_accounts,
):
    contract = prepared_case(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts[3]
    )
    with direct_vm.expect_revert("Invalid state"):
        contract.finalize_procurement_acceptance("case-1")
    assert contract.is_release_eligible("case-1") is False


def test_close_expired_uses_transaction_time_even_when_phase_is_stale(
    direct_vm,
    direct_deploy,
    direct_alice,
    direct_bob,
    direct_charlie,
    direct_accounts,
):
    contract = prepared_case(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts[3]
    )
    direct_vm.warp("2033-05-18T03:40:00Z")  # 2_000_000_400, exact final deadline
    direct_vm.sender = direct_alice
    contract.close_expired("case-1")
    assert contract.get_case("case-1")["state"] == "CLOSED_UNRESOLVED"
    assert contract.is_release_eligible("case-1") is False


def _digest(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def _semantic_result(status="ACCEPTED", unresolved="", cure="", failures="") -> str:
    # gltest auto-decodes a bare JSON mock into a dict, while this contract asks
    # exec_prompt for text. A short wrapper preserves the network response type.
    return "RESULT\n" + json.dumps({
        "status": status,
        "sample_ids": "sample-a|sample-b",
        "process_ids": "process-a",
        "criterion_ids": "criterion-a|criterion-b",
        "unresolved_ids": unresolved,
        "cure_target_ids": cure,
        "authority_failures": failures,
    })


def _evidence_ready_case(direct_vm, direct_deploy, buyer, vendor, primary, corroborating):
    policy = b"locked policy"
    first = b"primary report"
    second = b"corroborating report"
    direct_vm.warp("2033-05-18T03:33:20Z")
    direct_vm.sender = buyer
    contract = direct_deploy(CONTRACT)
    create_case(contract, buyer, vendor, primary, corroborating, _digest(policy))
    contract.activate_case("case-1")
    direct_vm.sender = primary
    contract.submit_evaluator_report(
        "case-1", "PRIMARY", "https://evidence.example/primary.json",
        _digest(first), "nonce-p", 2_000_000_000,
    )
    direct_vm.sender = corroborating
    contract.submit_evaluator_report(
        "case-1", "CORROBORATING", "https://evidence.example/corroborating.json",
        _digest(second), "nonce-c", 2_000_000_000,
    )
    direct_vm.mock_web(r"w3\.org/TR/", {"status": 200, "body": policy})
    direct_vm.mock_web(r"primary\.json", {"status": 200, "body": first})
    direct_vm.mock_web(r"corroborating\.json", {"status": 200, "body": second})
    return contract


def test_exact_evidence_and_valid_semantic_result_enable_one_time_acceptance(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts,
):
    contract = _evidence_ready_case(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts[3]
    )
    direct_vm.mock_llm(r"evaluating two independent", _semantic_result())
    direct_vm.sender = direct_alice
    contract.adjudicate("case-1", "attempt-1")
    verdict = contract.get_verdict("case-1")
    assert verdict["verdict"] == "ACCEPTED", verdict["authority_failures"]
    assert contract.is_release_eligible("case-1") is False
    contract.finalize_procurement_acceptance("case-1")
    assert contract.is_release_eligible("case-1") is True
    with direct_vm.expect_revert("Invalid state"):
        contract.finalize_procurement_acceptance("case-1")


def test_digest_mismatch_is_non_penalizing_unverifiable(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts,
):
    contract = _evidence_ready_case(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts[3]
    )
    direct_vm.clear_mocks()
    direct_vm.mock_web(r"w3\.org/TR/", {"status": 200, "body": b"wrong bytes"})
    direct_vm.sender = direct_alice
    contract.adjudicate("case-1", "attempt-1")
    assert contract.get_case("case-1")["state"] == "UNVERIFIABLE"
    assert contract.get_verdict("case-1")["authority_failures"]
    assert contract.is_release_eligible("case-1") is False


def test_invalid_validator_meaning_reverts_before_state_mutation(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts,
):
    contract = _evidence_ready_case(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie, direct_accounts[3]
    )
    direct_vm.mock_llm(
        r"evaluating two independent",
        _semantic_result("CURE_REQUIRED", "not-a-locked-finding", "not-a-locked-finding"),
    )
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("Unknown unresolved ID"):
        contract.adjudicate("case-1", "attempt-1")
    assert contract.get_case("case-1")["state"] == "EVIDENCE_READY"
    assert contract.get_verdict("case-1")["verdict"] == ""
