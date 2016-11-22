import os
import uuid

from ailoads.fmwk import scenario, requests

from connection_handler import ConnectionHandler

URL_SERVER = os.getenv('URL_SERVER',
                       'https://antenna.stage.mozaws.net')
DEBUG = True

_LINE = '---------------------------------'
_CONNECTIONS = {}
URL_DMPFILES = 'https://s3-us-west-2.amazonaws.com/fx-test-antenna'


def log_header(msg):
    print('{0}\n{1}\n{0}'.format(_LINE, msg))


def get_connection(id=None):
    if id is None or id not in _CONNECTIONS:
        id = uuid.uuid4().hex
        conn = ConnectionHandler(id, URL_SERVER)
        _CONNECTIONS[id] = conn

    return _CONNECTIONS[id]


def get_dmp_file(name_dmpfile):
    with open(name_dmpfile, 'wb') as handle:
        url = '{0}/{1}'.format(URL_DMPFILES, name_dmpfile)
        response = requests.get(url, stream=True)

        if not response.ok:
            print('ERROR: unable to download dmpfile from S3 --> Aborting!')
            exit()

        for block in response.iter_content(1024):
            handle.write(block)


@scenario(100)
def get_version():
    """Get version from Antenna server"""

    conn = get_connection('service-under-test')
    get_dmp_file('small.dmp')

    if DEBUG:
        log_header(list)
    resp = conn.get('/__version__')
    if DEBUG:
        print(resp.text)
    resp.raise_for_status()
