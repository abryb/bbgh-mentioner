import typing
from typing import NamedTuple

import requests
import settings

X = typing.TypeVar('X')


class ListResponse(typing.Generic[X]):
    def __init__(self, number_of_elements: int, items: typing.Iterator[X]):
        self.number_of_elements = number_of_elements
        self.items = items

    @staticmethod
    def from_data(data: dict, items_func):
        return ListResponse(data['numberOfElements'], map(items_func, data['content']))


class ApiError(ConnectionError):
    pass


class ApiArticle(NamedTuple):
    id: int
    content: str

    @staticmethod
    def from_data(data: dict) -> 'ApiArticle':
        return ApiArticle(
            id=data['id'],
            content=data['content']
        )


class ApiComment(NamedTuple):
    id: int
    content: str

    @staticmethod
    def from_data(data: dict) -> 'ApiComment':
        return ApiComment(
            id=data['id'],
            content=data['content']
        )


class ApiPlayer(NamedTuple):
    id: int
    first_name: str
    last_name: str

    @staticmethod
    def from_data(data: dict) -> 'ApiPlayer':
        return ApiPlayer(
            id=data['id'],
            first_name=data['firstName'],
            last_name=data['lastName']
        )

    def to_dict(self) -> dict:
        return self._asdict()

    @staticmethod
    def from_dict(data: dict) -> 'ApiPlayer':
        return ApiPlayer(
            id=data["id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )


class ApiMention(typing.NamedTuple):
    id: int
    comment: ApiComment
    player: ApiPlayer
    sentiment: str
    starts_at: int
    ends_at: int

    @staticmethod
    def from_data(data: dict) -> 'ApiMention':
        return ApiMention(
            id=data['id'],
            comment=ApiComment.from_data(data['comment']),
            player=ApiPlayer.from_data(data['player']),
            sentiment=data['sentiment'],
            starts_at=data['startsAt'],
            ends_at=data['endsAt']
        )


class ApiClient(object):
    def __init__(self, host):
        self.host = host

    def articles(self, page=0, size=20) -> ListResponse[ApiArticle]:
        data = self._get_list('/api/articles', {'page': page, 'size': size})
        return ListResponse.from_data(data, lambda x: ApiArticle.from_data(x))

    def all_articles(self) -> typing.Iterator[ApiArticle]:
        for item in self._all_items('/api/articles'):
            yield ApiArticle.from_data(item)

    def article_comments(self, article_id, page=0, size=20):
        data = self._get_list('/api/articles/{}/comments'.format(article_id), {'page': page, 'size': size})
        return ListResponse.from_data(data, lambda x: ApiComment.from_data(x))

    def all_article_comments(self, article_id) -> typing.Iterator[ApiComment]:
        for item in self._all_items('/api/articles/{}/comments'.format(article_id)):
            yield ApiComment.from_data(item)

    def all_players(self) -> typing.Iterator[ApiPlayer]:
        for item in self._all_items('/api/players'):
            yield ApiPlayer.from_data(item)

    def all_comment_mentions(self, comment_id : int) -> typing.Iterator[ApiMention]:
        for item in self._all_items('/api/comment/{}/mentions'.format(comment_id)):
            yield ApiMention.from_data(item)

    def create_mention(self, comment_id: int, player_id: int, starts_at=0, ends_at=0) -> ApiMention:
        r = self._post("/api/mentions", {
            "commentId": comment_id,
            "playerId": player_id,
            "startsAt": starts_at,
            "endsAt": ends_at
        })
        return ApiMention.from_data(r)

    def _post(self, path: str, json: dict):
        resp = requests.post(self.host + path, json=json)
        if resp.status_code not in [200, 201]:
            raise ApiError('POST {} {} {}'.format(path, resp.status_code, resp.json()))
        return resp.json()

    def _get_list(self, path: str, params) -> dict:
        resp = requests.get(self.host + path, params=params)
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET {} {}'.format(path, resp.status_code))
        return resp.json()

    def _all_items(self, path: str) -> typing.Iterator[dict]:
        items_per_page = 200
        count = items_per_page
        page = 0
        while count == items_per_page:
            items = self._get_list(path, {'page': page, 'size': items_per_page})
            page = page + 1
            count = items["numberOfElements"]
            for item in items['content']:
                yield item


api_client = ApiClient(settings.BBGH_BACKEND_URL)

