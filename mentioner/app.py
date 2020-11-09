from api_client import api_client
from mention_finder import mention_finder, Mention
import logging


class App(object):
    def create_all_mentions(self):
        api_client.all_articles()
        for article in api_client.all_articles():
            for comment in api_client.all_article_comments(article.id):
                for m in mention_finder.find_mentions(comment, article):
                    self.save_mention(m)

    def save_mention(self, mention: Mention) -> bool:
        for api_mention in api_client.all_comment_mentions(mention.comment_id):
            if api_mention.player.id == mention.player_id and api_mention.comment.id == mention.comment_id:
                return False  # mention already exists
        logging.info("Saving mention {}".format(mention))
        api_client.create_mention(mention.comment_id, mention.player_id)


app = App()
