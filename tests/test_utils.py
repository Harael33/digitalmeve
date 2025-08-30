from digitalmeve.utils import format_identity


def test_format_identity_valid():
    data = {'id': 'ABC123'}
    assert format_identity(data) == 'ABC123'


def test_format_identity_invalid():
    data = None
    assert format_identity(data) is None
