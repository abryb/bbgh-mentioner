import requests


class ApiError(ConnectionError):
    pass


class ApiClient:
    def __init__(self, host):
        self.host = host

    def articles(self):
        resp = requests.get(self.host + '/articles')
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /articles {}'.format(resp.status_code))
        print(resp.json())
