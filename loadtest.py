import os

from ailoads.fmwk import scenario

import utils

URL_SERVER = os.getenv('URL_SERVER',
                       'http://antenna.stage.mozaws.net')
DEBUG = False

if DEBUG:
    utils._log_everything()


@scenario(0)
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
