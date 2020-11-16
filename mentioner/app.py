from api_client import api_client
from mention_finder import Mention, MentionFinder
from text_finder import TextFinder
from morfeusz_wrapper import MorfeuszWrapper
from players_repository import PlayersRepository
import morfeusz2
import logging
import time
import settings
import os
import pickle


class App(object):
    __state = {}
    __state_file = '{}/app.pickle'.format(settings.CACHE_DIR)

    def __init__(self):
        self.__load_state()
        self.players_repository = PlayersRepository('{}/players.json'.format(settings.CACHE_DIR))
        self.mention_finder = MentionFinder(
            TextFinder(
                MorfeuszWrapper(
                    morfeusz2.Morfeusz(case_handling=morfeusz2.IGNORE_CASE)
                )
            ),
            self.players_repository
        )

    def create_all_mentions(self):
        if "create_all_mentions" not in self.__state:
            self.__state["create_all_mentions"] = {
                "last_article_id": 0
            }

        start_time = time.time()
        mentions_count = 0
        api_client.all_articles()
        for article in api_client.all_articles():
            if article.id <= self.__state["create_all_mentions"]["last_article_id"]:
                logging.debug("Skipping article {}".format(article.id))
                continue
            for comment in api_client.all_article_comments(article.id):
                logging.debug("Checking comment {} of article {}".format(comment.id, article.id))
                for m in self.mention_finder.find_mentions(comment, article):
                    mentions_count += 1
                    self.save_mention(m)
            self.__state["create_all_mentions"]["last_article_id"] = article.id
            logging.info("Done checking article {}".format(article.id))
        logging.info("Found {} mentions in {} seconds".format(mentions_count, time.time() - start_time))

    def save_mention(self, mention: Mention) -> bool:
        for api_mention in api_client.all_comment_mentions(mention.comment_id):
            if api_mention.player.id == mention.player_id \
                    and api_mention.comment.id == mention.comment_id \
                    and api_mention.starts_at == mention.starts_at \
                    and api_mention.ends_at == mention.ends_at:
                return False  # mention already exists
        logging.info("Saving mention {}".format(mention))
        api_client.create_mention(mention.comment_id, mention.player_id, mention.starts_at, mention.ends_at)

    def save_state(self):
        with open(self.__state_file, 'wb') as f:
            pickle.dump(self.__state, f)

    def __load_state(self):
        if not os.path.exists(self.__state_file):
            self.save_state()
            return

        with open(self.__state_file, 'rb') as f:
            self.__state = pickle.load(f)
