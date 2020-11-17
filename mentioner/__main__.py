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


def create_all_mentions():
    try:
        print("Creating all mentions")
        app.create_all_mentions()
        app.state.save()
        print("Done")
    except KeyboardInterrupt:
        print("\nCanceled by user. Saving state...")
        app.state.save()
        print("Bye.")


def state_info():
    print("Number of players: {}".format(len(app.state.players)))
    print("Last checked article id: {}".format(app.state.create_all_mentions_last_article_id))


actions = {
    "download_players": download_players,
    "create_all_mentions": create_all_mentions,
    "state_info": state_info
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
