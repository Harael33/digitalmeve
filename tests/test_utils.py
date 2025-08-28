import pytest
from digitalmeve.utils import format_identity

def test_format_identity_returns_dict():
    data = {"name": "John", "age": 30}
    result = format_identity(data)
    assert isinstance(result, dict)
    assert "name" in result
    assert result["name"] == "John"
