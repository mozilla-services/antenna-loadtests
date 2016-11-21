import os

from ailoads.fmwk import scenario

import utils

URL_SERVER = os.getenv('URL_SERVER',
                       'http://antenna.stage.mozaws.net')
URL_DMPFILES = 'https://s3-us-west-2.amazonaws.com/fx-test-antenna'
DEBUG = True

_LINE = '---------------------------------'
_CONNECTIONS = {}

# utils._log_everything()


def log_header(msg):
    print('{0}\n{1}\n{0}'.format(_LINE, msg))


@scenario(0)
def test_get_version():
    """Get version from Antenna server"""
    conn = get_connection('service-under-test')
    resp = conn.get('/__version__')
    if DEBUG:
        print(resp.status_code)
        print(resp.headers)
        print(resp.text)
    resp.raise_for_status()


@scenario(0)
def test_post_empty_dmp():
    crash_payload = utils.assemble_crash_payload(
        raw_crash={'ProductName': 'Firefox', 'Version': '1'},
        dumps={}
    )
    resp = utils.post_crash(
        url=URL_SERVER,
        crash_payload=crash_payload)
    print('test_post_empty_dmp: %s' % resp)
    resp.raise_for_status()


@scenario(100)
def test_crash_400k_uncompressed():
    size = (400 * 1024)
    raw_crash, dumps = utils.generate_sized_crashes(size)
    crash_payload = utils.assemble_crash_payload(raw_crash, dumps)
    resp = utils.post_crash(URL_SERVER, crash_payload)
    print("test_crash_400k_uncompressed: %s" % resp)
    resp.raise_for_status()


@scenario(0)
def test_crash_4mb_uncompressed():
    size = (4 * 1024 * 1024)
    raw_crash, dumps = utils.generate_sized_crashes(size)
    crash_payload = utils.assemble_crash_payload(raw_crash, dumps)
    payload, headers = utils.multipart_encode(crash_payload)

    if len(payload) != size:
        raise ValueError('payload size %s', len(payload))

    resp = utils.post_crash(URL_SERVER, crash_payload)
    print("test_crash_4mb_uncompressed: %s" % resp)
    resp.raise_for_status()


@scenario(0)
def test_crash_20mb_uncompressed():
    size = (20 * 1024 * 1024)
    raw_crash, dumps = utils.generate_sized_crashes(size)
    crash_payload = utils.assemble_crash_payload(raw_crash, dumps)
    payload, headers = utils.multipart_encode(crash_payload)

    if len(payload) != size:
        raise ValueError('payload size %s', len(payload))

    resp = utils.post_crash(URL_SERVER, crash_payload)
    print("test_crash_20mb_uncompressed: %s" % resp)
    resp.raise_for_status()


@scenario(0)
def test_crash_greater_than_20mb_uncompressed():
    size = (50 * 1024 * 1024)
    raw_crash, dumps = utils.generate_sized_crashes(size)
    crash_payload = utils.assemble_crash_payload(raw_crash, dumps)
    payload, headers = utils.multipart_encode(crash_payload)

    if len(payload) != size:
        raise ValueError('payload size %s', len(payload))
    resp = utils.post_crash(URL_SERVER, crash_payload)
    print("test_crash_greater_than_20mb_uncompressed: %s" % resp)
    resp.raise_for_status()
