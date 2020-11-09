from api_client import api_client, ApiPlayer
import typing
import json
import settings
import os
import logging


class PlayersRepository(object):
    players = list()
    indexes = {
        "full_name": {}
    }
    cache_file = '{}/players.json'.format(settings.CACHE_DIR)

    def __init__(self):
        self.load_players()

    def load_players(self):
        if not os.path.exists(self.cache_file):
            self.download_players()
            self.save_cache_file()
        else:
            self.load_cache_file()
        self.create_indexes()

    def download_players(self):
        logging.info("Downloading players...")
        for player in api_client.all_players():
            self.players.append(player)

    def save_cache_file(self):
        with open(self.cache_file, 'w') as f:
            json_players = list(map(lambda x: x.to_dict(), self.players))
            json.dump(json_players, f)

    def load_cache_file(self):
        if not os.path.exists(self.cache_file):
            raise Exception("File {} does not exist".format(self.cache_file))

        with open(self.cache_file, 'r') as outfile:
            self.players = list(map(lambda x: ApiPlayer.from_dict(x), json.load(outfile)))

    def create_indexes(self):
        for i, player in enumerate(self.players):
            full_name = "{} {}".format(player.first_name, player.last_name)

            if full_name in self.indexes["full_name"]:
                self.indexes["full_name"][full_name].append(i)
            else:
                self.indexes["full_name"][full_name] = [i]

    def find_by_full_name(self, full_name: str) -> typing.List[ApiPlayer]:
        if full_name in self.indexes["full_name"]:
            return list(map(lambda i: self.players[i], self.indexes["full_name"][full_name]))
        else:
            return list()


players_repository = PlayersRepository()
