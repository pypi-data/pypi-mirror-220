import unittest

from codsUtils import is_creditcode


class TestSimple(unittest.TestCase):

    def test_is_creditcode(self):
        self.assertEqual(is_creditcode(1), False)

if __name__ == '__main__':
    unittest.main()
