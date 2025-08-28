import pytest
from digitalmeve.verifier import verify_identity

def test_verify_identity_valid():
    data = {"name": "Alice", "verified": True}
    result = verify_identity(data)
    assert result is True

def test_verify_identity_invalid():
    data = {"name": "Bob", "verified": False}
    result = verify_identity(data)
    assert result is False
