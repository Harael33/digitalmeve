import pytest
from digitalmeve.generator import generate_meve

def test_generate_meve_returns_string():
    result = generate_meve("test")
    assert isinstance(result, str)
    assert "test" in result
