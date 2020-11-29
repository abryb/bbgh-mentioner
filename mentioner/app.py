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

    def create_mentions(self):
        action_summary = dict(articles=0, comments=0, mentions=0, start_time=time.time())
        self.api_client.all_articles()
        # TODO change for updateDate when it comes
        for article in self.api_client.all_articles(sort='creationDate,ASC'):
            action_summary['articles'] += 1
            if article.creation_date <= self.state.create_mentions_last_checked:
                logging.debug("Skipping article {}".format(article.id))
                continue
            for comment in self.api_client.all_article_comments(article.id):
                logging.debug("Checking comment {} of article {}".format(comment.id, article.id))
                for m in self.mention_finder.find_mentions(comment, article):
                    action_summary['comments'] += 1
                    self.__save_mention(m)
            self.state.create_mentions_last_checked = article.update_date
            logging.info("Done checking article {}".format(article.id))
        logging.info("Checked {} article and {} comments. Found {} mentions in {} seconds.".format(
            action_summary['articles'],
            action_summary['comments'],
            action_summary['mentions'],
            time.time() - action_summary['start_time']))

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
        self.create_mentions_last_checked = datetime.datetime.fromtimestamp(0)
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
