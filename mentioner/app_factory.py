import os
from mentioner.app import App
from dotenv import load_dotenv
load_dotenv()


BBGH_BACKEND_URL = os.getenv("BBGH_BACKEND_URL")
CACHE_DIR = dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/cache"


def create_app(
        state_file="{}/app.pickle".format(CACHE_DIR),
        api_url=BBGH_BACKEND_URL) -> App:

    return App(state_file, api_url)
