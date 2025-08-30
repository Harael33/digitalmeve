import pytest
from digitalmeve.utils import format_identity


def test_format_identity_valid():
    assert format_identity("ABC123") == "ABC123"


def test_format_identity_invalid():
    assert format_identity(None) is None
