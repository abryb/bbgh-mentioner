from api_client import api_client, ApiPlayer
import typing
import os
import logging
import pickle


class PlayersRepository(object):
    __state = {
        "players": list(),
        "indexes": {
            "full_name": {}
        }

    }

    def __init__(self, state_file: str):
        self.__state_file = state_file
        self.__load_state()

    def find_by_full_name(self, full_name: str) -> typing.List[ApiPlayer]:
        if full_name in self.__state['indexes']["full_name"]:
            return list(map(lambda i: self.__state['players'][i], self.__state['indexes']["full_name"][full_name]))
        else:
            return list()

    def __download_players(self):
        logging.info("Downloading players...")
        for player in api_client.all_players():
            self.__state['players'].append(player)
        self.__create_indexes()

    def __create_indexes(self):
        for i, player in enumerate(self.__state['players']):
            full_name = "{} {}".format(player.first_name, player.last_name)

            if full_name in self.__state['indexes']["full_name"]:
                self.__state['indexes']["full_name"][full_name].append(i)
            else:
                self.__state['indexes']["full_name"][full_name] = [i]

    def save_state(self):
        with open(self.__state_file, 'wb') as f:
            pickle.dump(self.__state, f)

    def __load_state(self):
        if not os.path.exists(self.__state_file):
            self.__download_players()
            self.save_state()
            return

        with open(self.__state_file, 'rb') as f:
            self.__state = pickle.load(f)

