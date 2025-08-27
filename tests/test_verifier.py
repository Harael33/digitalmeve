import unittest
from src import verifier, generator

class TestVerifier(unittest.TestCase):

    def test_verification_flow(self):
        # Générer un fichier de test
        dummy_content = b"Document de test"
        proof = generator.generate_proof(dummy_content, issuer="TestUser")

        # Vérifier que le fichier généré est valide
        result = verifier.verify_proof(proof, dummy_content)
        self.assertTrue(result)

    def test_tampered_document(self):
        dummy_content = b"Document original"
        proof = generator.generate_proof(dummy_content, issuer="TestUser")

        # Document modifié
        tampered_content = b"Document modifie"
        result = verifier.verify_proof(proof, tampered_content)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
