import unittest
import tempfile
import os

from app import AppState


class FinderTestCase(unittest.TestCase):
    def test_can_save_state(self):
        state_file = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()))

        app_state = AppState(state_file)

        app_state.create_all_mentions_last_article_id = 2
        app_state.save()

        app_state_2 = AppState(state_file)
        self.assertEqual(app_state_2.create_all_mentions_last_article_id, 2)


if __name__ == '__main__':
    unittest.main()
