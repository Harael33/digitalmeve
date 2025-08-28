from digitalmeve.verifier import verify_identity

def test_verify_identity_valid():
    result = verify_identity("alice", expected_issuer="alice")
    assert result is True

def test_verify_identity_invalid():
    result = verify_identity("bob", expected_issuer="alice")
    assert result is False
