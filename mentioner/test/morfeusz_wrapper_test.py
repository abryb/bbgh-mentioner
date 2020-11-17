import unittest

from mentioner.morfeusz import morfeusz_wrapper


class MorfeuszTestCase(unittest.TestCase):
    def test_can_update_index(self):
        index = morfeusz_wrapper._update_index("A very big snowball is coming.", 2, "big")
        self.assertEqual(index, 7)

        index = morfeusz_wrapper._update_index("A very big snowball is coming.", 2, "coming")
        self.assertEqual(index, 23)


if __name__ == '__main__':
    unittest.main()
