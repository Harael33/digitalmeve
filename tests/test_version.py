from importlib import metadata
import digitalmeve

def test_version():
    # Vérifie que __version__ du module = version installée du package
    assert digitalmeve.__version__ == metadata.version("digitalmeve")
