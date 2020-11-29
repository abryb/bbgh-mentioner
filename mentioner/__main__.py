import sys
import argparse
import logging
sys.path.append(".")
from mentioner.app_factory import create_app


def download_players():
    try:
        print("Downloading all players...")
        app.download_players()
        app.state.save()
        print("Done")
    except KeyboardInterrupt:
        app.state.save()
        print("\nAborted. Bye.")


def create_mentions():
    try:
        print("Creating all mentions")
        app.create_mentions()
        app.state.save()
        print("Done")
    except KeyboardInterrupt:
        print("\nCanceled by user. Saving state...")
        app.state.save()
        print("Bye.")


def state_info():
    print("Number of players: {}".format(len(app.state.players)))
    print("Last checked article update date: {}".format(app.state.create_mentions_last_checked))


def clear_state():
    try:
        print("Clearing app state...")
        app.clear_state()
        app.state.save()
        print("Done")
    except KeyboardInterrupt:
        print("\nAborted. Bye.")


actions = {
    "download_players": download_players,
    "create_mentions": create_mentions,
    "state_info": state_info,
    "clear_state": clear_state
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('action', help='action to call', choices=actions.keys())
    parser.add_argument('--verbose', '-v', dest="verbose", help='Verbose output, -vv very verbose', action='count', default=0)

    args = parser.parse_args()
    action = args.action

    if args.verbose == 1:
        logging.basicConfig(level=logging.INFO)
    elif args.verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)

    app = create_app()

    actions[action]()

    sys.exit(0)
