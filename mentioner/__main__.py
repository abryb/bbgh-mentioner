import sys
import os
import argparse
import logging
import datetime
from dotenv import load_dotenv
sys.path.append(".")
from mentioner.app_factory import create_app


def writeln(message):
    print("{}: {}".format(datetime.datetime.now(), message))


def download_players():
    try:
        writeln("Downloading all players...")
        app.download_players()
        app.state.save()
        writeln("Done")
    except KeyboardInterrupt:
        app.state.save()
        writeln("\nAborted. Bye.")


def create_mentions():
    try:
        writeln("Creating mentions for articles updated after {}".format(app.state.create_mentions_last_updated_at))
        action_summary = app.create_mentions()
        app.state.save()
        writeln("Checked {} article and {} comments. Found {} mentions in {} seconds.".format(
            action_summary['articles'],
            action_summary['comments'],
            action_summary['mentions'],
            action_summary['duration']))
    except KeyboardInterrupt:
        writeln("\nCanceled by user. Saving state...")
        app.state.save()
        writeln("Bye.")


def state_info():
    writeln("Number of players: {}".format(len(app.state.players)))
    writeln("Last checked article update date: {}".format(app.state.create_mentions_last_updated_at))


def clear_state():
    try:
        writeln("Clearing app state...")
        app.clear_state()
        app.state.save()
        writeln("Done")
    except KeyboardInterrupt:
        writeln("\nAborted. Bye.")


def run():
    try:
        if len(app.state.players) == 0:
            download_players()
        create_mentions()
    except KeyboardInterrupt:
        writeln("\nAborted. Bye.")


actions = {
    "run": run,
    "download_players": download_players,
    "create_mentions": create_mentions,
    "state_info": state_info,
    "clear_state": clear_state
}


if __name__ == '__main__':
    # load .env
    load_dotenv()
    # load .env.local
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env.local'))

    BBGH_BACKEND_URL = os.getenv("BBGH_BACKEND_URL")
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('action', help='action to call', choices=actions.keys())
    parser.add_argument('--verbose', '-v', dest="verbose", help='Verbose output, -vv very verbose', action='count', default=0)

    args = parser.parse_args()
    action = args.action

    # resolve logging level
    if args.verbose == 1:
        LOGGING_LEVEL = logging.INFO
    elif args.verbose >= 2:
        LOGGING_LEVEL = logging.DEBUG

    logging.basicConfig(level=LOGGING_LEVEL)

    app = create_app(load_env_file=False)

    actions[action]()

    sys.exit(0)
