from src import utils

def verify_proof(proof: dict, content: bytes) -> bool:
    """
    Vérifie qu’un document correspond bien à une preuve donnée.
    """
    expected_hash = proof.get("hash")
    actual_hash = utils.compute_hash(content)

    return expected_hash == actual_hash
