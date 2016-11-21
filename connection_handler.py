import requests


TIMEOUT = 30


class ConnectionHandler(object):

    def __init__(self, id, url_server):
        self.id = id
        self.url_server = url_server
        self.timeout = TIMEOUT

    def post(self, endpoint, data):
        return requests.post(
            self.url_server + endpoint,
            data=data,
            timeout=self.timeout)

    def get(self, endpoint):
        return requests.get(
            self.url_server + endpoint,
            timeout=self.timeout)

    def delete(self, endpoint):
        return requests.delete(
            self.url_server + endpoint,
            timeout=self.timeout)
