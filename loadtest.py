import os
import uuid

from ailoads.fmwk import scenario, requests

from connection_handler import ConnectionHandler

URL_SERVER = os.getenv('URL_SERVER',
                       'https://antenna.stage.mozaws.net')
DEBUG = True

_LINE = '---------------------------------'
_CONNECTIONS = {}

PERCENTAGE = 100
# curl -k  --data "mozstd-track-digest256;a:1" https://shavar.stage.mozaws.net/downloads # noqa


def log_header(msg):
    print('{0}\n{1}\n{0}'.format(_LINE, msg))


def get_connection(id=None):
    if id is None or id not in _CONNECTIONS:
        id = uuid.uuid4().hex
        conn = ConnectionHandler(id, URL_SERVER)
        _CONNECTIONS[id] = conn

    return _CONNECTIONS[id]


@scenario(PERCENTAGE)
def get_version():
    """Get version from Antenna server"""

    conn = get_connection('service-under-test')

    if DEBUG:
        log_header(list)
    resp = conn.get('/__version__')
    if DEBUG:
        print(resp.text)
    resp.raise_for_status()
