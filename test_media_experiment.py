import unittest

from media_experiment import stable_bucket


class StableBucketTest(unittest.TestCase):
    def test_same_identity_has_same_bucket(self):
        first = stable_bucket("listener-101", "media-player-ab")
        second = stable_bucket("listener-101", "media-player-ab")
        self.assertEqual(first, second)
        self.assertGreaterEqual(first, 0)
        self.assertLess(first, 100)


if __name__ == "__main__":
    unittest.main()
