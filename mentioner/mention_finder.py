import typing
from api_client import ApiArticle, ApiComment, api_client
from text_finder import finder
from players_repository import players_repository


class Mention(typing.NamedTuple):
    person: tuple
    comment_id: int
    article_id: int
    player_id: int


class MentionFinder(object):
    def find_mentions(self, comment: ApiComment, article: ApiArticle) -> typing.Set[Mention]:
        mentions = set()
        for mention in self.find_mentions_by_comment_has_last_name_of_full_name_in_article(comment, article):
            mentions.add(mention)

        return mentions

    def find_mentions_by_comment_has_last_name_of_full_name_in_article(self, comment: ApiComment, article: ApiArticle):
        for last_name in finder.find_last_names(comment.content):
            for full_names_in_article in finder.find_full_names(article.content):
                full_name = full_names_in_article[0] + " " + full_names_in_article[1]
                if full_names_in_article[1] == last_name:
                    players = players_repository.find_by_full_name(full_name)
                    if len(players) == 1:
                        yield Mention(
                            person=full_names_in_article,
                            comment_id=comment.id,
                            article_id=article.id,
                            player_id=players[0].id
                        )




mention_finder = MentionFinder()
