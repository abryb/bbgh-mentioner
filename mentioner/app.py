import os
import pickle
from mentioner.api.client import ApiClient
from mentioner.finder.mention import Mention, MentionFinder
from mentioner.finder.text import TextFinder
from mentioner.morfeusz import morfeusz_wrapper
from mentioner.repository.players import PlayersRepository
import logging
import time


class App(object):
    def __init__(self, state_file: str, api_url: str):
        self.state = AppState(state_file)
        self.api_client = ApiClient(api_url)
        self.players_repository = PlayersRepository(self.state.players)
        self.morfeusz_wrapper = morfeusz_wrapper
        self.text_finder = TextFinder(self.morfeusz_wrapper)
        self.mention_finder = MentionFinder(self.text_finder, self.players_repository)

    def download_players(self):
        logging.info("Downloading players...")
        for player in self.api_client.all_players():
            self.players_repository.add_player(player)
        logging.info("Done downloading players.")

    def create_all_mentions(self):
        start_time = time.time()
        mentions_count = 0
        self.api_client.all_articles()
        for article in self.api_client.all_articles():
            if article.id <= self.state.create_all_mentions_last_article_id:
                logging.debug("Skipping article {}".format(article.id))
                continue
            for comment in self.api_client.all_article_comments(article.id):
                logging.debug("Checking comment {} of article {}".format(comment.id, article.id))
                for m in self.mention_finder.find_mentions(comment, article):
                    mentions_count += 1
                    self.__save_mention(m)
            self.state.create_all_mentions_last_article_id = article.id
            logging.info("Done checking article {}".format(article.id))
        logging.info("Found {} mentions in {} seconds".format(mentions_count, time.time() - start_time))

    def __save_mention(self, mention: Mention) -> bool:
        for api_mention in self.api_client.all_comment_mentions(mention.comment_id):
            if api_mention.player.id == mention.player_id \
                    and api_mention.comment.id == mention.comment_id \
                    and api_mention.starts_at == mention.starts_at \
                    and api_mention.ends_at == mention.ends_at:
                return False  # mention already exists
        logging.info("Saving mention {}".format(mention))
        self.api_client.create_mention(mention.comment_id, mention.player_id, mention.starts_at, mention.ends_at)


class AppState(object):
    def __init__(self, file_path: str):
        self.file_path = file_path

        self.create_all_mentions_last_article_id = 0
        self.players = {}

        self.load()

    def save(self):
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
        with open(self.file_path, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def load(self):
        if not os.path.exists(self.file_path):
            return

        with open(self.file_path, 'rb') as f:
            # self.data = {**self.data, **pickle.load(f)}
            self.__dict__.update(pickle.load(f))
