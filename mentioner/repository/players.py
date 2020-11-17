from mentioner.api.client import ApiPlayer, ApiClient
import typing


class PlayersRepository(object):
    def __init__(self, players: dict):
        self.full_name_index = {}
        self.players = players
        for _, player in players.items():
            self.add_player(player)

    def find_by_full_name(self, full_name: str) -> typing.List[ApiPlayer]:
        if full_name in self.full_name_index:
            return self.full_name_index[full_name]
        else:
            return list()

    def add_player(self, player: ApiPlayer):
        self.players[player.id] = player
        # add to full name index
        full_name = "{} {}".format(player.first_name, player.last_name)
        if full_name in self.full_name_index:
            self.full_name_index[full_name].append(player)
        else:
            self.full_name_index[full_name] = [player]
