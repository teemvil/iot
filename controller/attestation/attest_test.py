import unittest
import attest

class AttestTesting(unittest.TestCase):

    """
    Should fail because hostname is not correct.
    """
    def test_create_dict(self):
        o = attest.create_dict({'hostname': '123'}, 123)
        self.assertEqual(o, {})

if __name__ == '__main__':
    unittest.main()