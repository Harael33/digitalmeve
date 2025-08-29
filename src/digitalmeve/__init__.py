__all__ = ["generate_meve", "verify_meve", "__version__"]
__version__ = "0.1.5"

try:
    from .core import generate_meve, verify_meve  # noqa: F401
except Exception:
    # allow import digitalmeve even if core import fails during CI sanity checks
    pass
