import digitalmeve as dm

def test_version():
    # La version interne doit correspondre à ce qu’on a défini dans __init__.py
    assert dm.__version__ == "0.1.4"
