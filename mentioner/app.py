import os
import pickle
from mentioner.api.client import ApiClient
from mentioner.finder.mention import Mention, MentionFinder
from mentioner.finder.text import TextFinder
from mentioner.morfeusz import morfeusz_wrapper
from mentioner.repository.players import PlayersRepository
import logging
import time
import datetime


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

    def create_mentions(self) -> dict:
        action_summary = dict(articles=0, comments=0, mentions=0, start_time=time.time(), duration=None)
        current_updated_at = datetime.datetime.fromtimestamp(0)
        for article in self.api_client.all_articles_updated_after(self.state.create_mentions_last_updated_at):
            if article.updated_at < self.state.create_mentions_last_updated_at:
                logging.debug("Skipping article {}".format(article.id))
                continue
            action_summary['articles'] += 1
            for comment in self.api_client.all_article_comments(article.id):
                logging.debug("Checking comment {} of article {} updated at {}".format(comment.id, article.id, article.updated_at))
                action_summary['comments'] += 1
                for m in self.mention_finder.find_mentions(comment, article):
                    action_summary['mentions'] += 1
                    self.__save_mention(m)
            if current_updated_at < article.updated_at:
                # If we are done checking some updated_at value (many articles can have same updatedAt) we can save it
                self.state.create_mentions_last_updated_at = article.updated_at
                current_updated_at = article.updated_at
            logging.info("Done checking article {} updated at {}".format(article.id, article.updated_at))
        action_summary['duration'] = time.time() - action_summary['start_time']
        logging.info("Finished create_mentions. Action summary: {}".format(action_summary))
        return action_summary

    def clear_state(self):
        file_path = self.state.file_path
        if os.path.exists(file_path):
            os.remove(file_path)
        self.state = AppState(file_path)

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
        self.create_mentions_last_updated_at = datetime.datetime.fromtimestamp(0)
        self.players = dict()
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
            self.__dict__.update(pickle.load(f))