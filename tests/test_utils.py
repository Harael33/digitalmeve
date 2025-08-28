from digitalmeve.utils import format_identity

def test_format_identity_with_str():
    assert format_identity(" Alice ") == "alice"

def test_format_identity_with_none():
    assert format_identity(None) == ""

def test_format_identity_with_dict():
    result = format_identity({"name": "Alice"})
    assert isinstance(result, str)
    assert "alice" in result.lower()
