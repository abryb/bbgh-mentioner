import unittest

from mentioner.finder import TextFinder
from mentioner.morfeusz import morfeusz_wrapper

finder = TextFinder(morfeusz_wrapper)


class FinderTestCase(unittest.TestCase):
    def test_can_find_name_and_lastname(self):
        self.assertEqual(finder.find_full_names(""), list())
        example = finder.find_full_names(u"Jan Kowalski je ciastka")
        self.assertEqual((u'Jan', u'Kowalski'), example[0].result)

    def test_can_find_last_name(self):
        self.assertGreater(len(finder.find_last_names("Co za Kowalski!")), 0)

    def test_can_find_lower_case_letter_last_name(self):
        self.assertGreater(len(finder.find_last_names("Co za Kowalski!")), 0)


if __name__ == '__main__':
    unittest.main()
