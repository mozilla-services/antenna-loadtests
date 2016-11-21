import os
import uuid

from ailoads.fmwk import scenario, requests

URL_SERVER = os.getenv('URL_SERVER',
                       'https://shavar.stage.mozaws.net')
TIMEOUT = 30
DEBUG = True

_LINE = '---------------------------------'
_CONNECTIONS = {}
_LISTS = [
    "base-track-digest256",
    "baseeff-track-digest256",
    "basew3c-track-digest256",
    "content-track-digest256",
    "contenteff-track-digest256",
    "contentw3c-track-digest256",
    "mozfull-track-digest256",
    "mozfullstaging-track-digest256",
    "mozplugin-block-digest256",
    "mozplugin2-block-digest256",
    "mozstd-track-digest256",
    "mozstd-trackwhite-digest256",
    "mozstdstaging-track-digest256",
    "mozstdstaging-trackwhite-digest256",
    "moztestpub-track-digest256",
    "moztestpub-trackwhite-digest256"
]

PERCENTAGE = 100
# curl -k  --data "mozstd-track-digest256;a:1" https://shavar.stage.mozaws.net/downloads # noqa


def log_header(msg):
    print('{0}\n{1}\n{0}'.format(_LINE, msg))


def get_connection(id=None):
    if id is None or id not in _CONNECTIONS:
        id = uuid.uuid4().hex
        conn = ShavarConnection(id)
        _CONNECTIONS[id] = conn

    return _CONNECTIONS[id]


class ShavarConnection(object):

    def __init__(self, id):
        self.id = id
        self.timeout = TIMEOUT

    def post(self, endpoint, data):
        return requests.post(
            URL_SERVER + endpoint,
            data=data,
            timeout=self.timeout)

    def get(self, endpoint):
        return requests.get(
            URL_SERVER + endpoint,
            timeout=self.timeout)

    def delete(self, endpoint):
        return requests.delete(
            URL_SERVER + endpoint,
            timeout=self.timeout)


@scenario(PERCENTAGE)
def get_lists():
    """Get TP lists from shavar server"""

    conn = get_connection('mozstd_track_digest256')
    for list in _LISTS:

        if DEBUG:
            log_header(list)
        data = '{0};a:1'.format(list)
        resp = conn.post('/downloads', data)
        if DEBUG:
            print(resp.text)
        resp.raise_for_status()
