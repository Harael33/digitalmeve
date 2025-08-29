from digitalmeve import generate_meve, verify_meve


def test_generate_meve():
    result = generate_meve()
    assert isinstance(result, str)
    assert result == "generated"


def test_verify_meve():
    result = verify_meve()
    assert isinstance(result, bool)
    assert result is True
