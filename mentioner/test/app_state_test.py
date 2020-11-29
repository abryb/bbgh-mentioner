import unittest
import tempfile
import os

from app import AppState


class AppStateTest(unittest.TestCase):
    def test_can_save_state(self):
        state_file = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()))

        app_state = AppState(state_file)

        app_state.checked_articles = {1: {}, 2: {}}
        app_state.save()

        app_state_2 = AppState(state_file)
        self.assertEqual(len(app_state_2.checked_articles), 2)


if __name__ == '__main__':
    unittest.main()
