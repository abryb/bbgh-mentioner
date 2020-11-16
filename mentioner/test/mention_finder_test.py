import unittest

from mention_finder import mention_finder


class FinderTestCase(unittest.TestCase):
    def test_find_mentions_by_comment_has_last_name_of_full_name_in_article(self):
        mention_finder.find_mentions_by_comment_has_last_name_of_full_name_in_article()
        self.assertEqual(mention_finder.find_full_names(""), list())
        example = mention_finder.find_full_names(u"Jan Kowalski je ciastka")
        self.assertEqual((u'Jan', u'Kowalski'), example[0].result)

    def test_can_find_last_name(self):
        self.assertGreater(len(mention_finder.find_last_names("Co za Kowalski!")), 0)

    def test_can_find_lower_case_letter_last_name(self):
        self.assertGreater(len(mention_finder.find_last_names("Co za kowalski!")), 0)


if __name__ == '__main__':
    unittest.main()
