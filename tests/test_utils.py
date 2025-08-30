import pytest
from digitalmeve.utils import format_identity


def test_format_identity_valid():
    # l'implémentation attend une clé 'identity'
    data = {"identity": "ABC123"}
    assert format_identity(data) == "ABC123"


def test_format_identity_invalid():
    # l'implémentation ne gère pas None -> AttributeError attendu
    with pytest.raises(AttributeError):
        format_identity(None)
