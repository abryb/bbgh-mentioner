import unittest

from text_finder import finder


class FinderTestCase(unittest.TestCase):
    def test_can_find_name_and_lastname(self):
        self.assertEqual(finder.find_full_names(""), set())
        self.assertEqual({(u'Jan', u'Kowalski')}, finder.find_full_names(u"Jan Kowalski je ciastka"))


if __name__ == '__main__':
    unittest.main()
