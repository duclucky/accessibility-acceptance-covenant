def test_direct_loader_probe(direct_deploy):
    contract = direct_deploy("tests/fixtures/minimal_contract.py")
    assert contract.get_value() == "ok"
