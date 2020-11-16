import typing
from api_client import ApiArticle, ApiComment
from text_finder import TextFinder
from players_repository import PlayersRepository
from unidecode import unidecode


class Mention(typing.NamedTuple):
    person: tuple
    comment_id: int
    article_id: int
    player_id: int
    starts_at: int
    ends_at: int


class MentionFinder(object):

    def __init__(self, text_finder: TextFinder, players_repository: PlayersRepository):
        self.players_repository = players_repository
        self.text_finder = text_finder

    __article_full_names_cache = {}

    def find_mentions(self, comment: ApiComment, article: ApiArticle) -> typing.Set[Mention]:
        mentions = set()
        for mention in self.find_mentions_by_comment_has_last_name_of_full_name_in_article(comment, article):
            mentions.add(mention)

        return mentions

    def find_mentions_by_comment_has_last_name_of_full_name_in_article(self, comment: ApiComment, article: ApiArticle):
        for last_name_in_comment in self.text_finder.find_last_names(comment.content):
            for full_name_in_article in self.__article_full_names(article):
                # converting "Łąkowski" to 'lakowski'
                last_name_in_comment_normalized = unidecode(last_name_in_comment.result.lower())
                last_name_in_article_normalized = unidecode(full_name_in_article.result.last_name.lower())
                if last_name_in_article_normalized == last_name_in_comment_normalized:
                    players = self.players_repository.find_by_full_name(full_name_in_article.result.full_name())
                    if len(players) == 1:
                        yield Mention(
                            person=full_name_in_article.result,
                            comment_id=comment.id,
                            article_id=article.id,
                            player_id=players[0].id,
                            starts_at=last_name_in_comment.starts_at,
                            ends_at=last_name_in_comment.ends_at
                        )

    def __article_full_names(self, article: ApiArticle):
        if article.id not in self.__article_full_names_cache:
            self.__article_full_names_cache[article.id] = self.text_finder.find_full_names(article.content)
        return self.__article_full_names_cache[article.id]
