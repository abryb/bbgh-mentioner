import os
from mentioner.app import App
from dotenv import load_dotenv


def create_app(load_env_file=True) -> App:
    if load_env_file:
        # load .env
        load_dotenv()
        # load .env.local
        load_dotenv(os.path.join(os.path.dirname(__file__), '.env.local'))

    state_file = os.path.dirname(__file__) + "/../cache/app.pickle"
    api_url = os.getenv("BBGH_BACKEND_URL")

    return App(state_file, api_url)
