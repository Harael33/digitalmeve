import unittest
from src import utils

class TestUtils(unittest.TestCase):

    def test_hash_function(self):
        data = b"hello world"
        h = utils.compute_hash(data)
        self.assertEqual(len(h), 64)  # SHA-256 fait 64 caractères hex

    def test_id_generation(self):
        unique_id = utils.generate_id()
        self.assertTrue(isinstance(unique_id, str))
        self.assertGreater(len(unique_id), 5)

if __name__ == "__main__":
    unittest.main()
