import os

from ailoads.fmwk import scenario

import utils

URL_SERVER = os.getenv('URL_SERVER',
                       'https://antenna.dev.mozaws.net/submit')
DEBUG = False

if DEBUG:
    utils._log_everything()


@scenario(0)
def test_crash_100k_compressed():
    size = (100 * 1024)
    raw_crash, dumps = utils.generate_sized_crashes(size)
    # Generate the payload and headers for a crash
    payload, headers = utils.multipart_encode(raw_crash)
    crash_payload = utils.assemble_crash_payload(raw_crash, dumps)
    # POST the dump to Antenna
    resp = utils.post_crash(URL_SERVER, crash_payload, compressed=True)
    print("test_crash_100k_compressed: HTTP %s" % resp.status_code)
    # Verify HTTP 200
    resp.raise_for_status()
    # Verify the response text contains a CrashID
    utils.verify_crashid(resp.text)


@scenario(0)
def test_crash_150k_compressed():
    size = (150 * 1024)
    raw_crash, dumps = utils.generate_sized_crashes(size)
    # Generate the payload and headers for a crash
    payload, headers = utils.multipart_encode(raw_crash)
    crash_payload = utils.assemble_crash_payload(raw_crash, dumps)
    # POST the dump to Antenna
    resp = utils.post_crash(URL_SERVER, crash_payload, compressed=True)
    print("test_crash_150k_compressed: HTTP %s" % resp.status_code)
    # Verify HTTP 200
    resp.raise_for_status()
    # Verify the response text contains a CrashID
    utils.verify_crashid(resp.text)


@scenario(0)
def test_crash_400k_uncompressed():
    size = (400 * 1024)
    raw_crash, dumps = utils.generate_sized_crashes(size)
    crash_payload = utils.assemble_crash_payload(raw_crash, dumps)
    # POST the dump to Antenna
    resp = utils.post_crash(URL_SERVER, crash_payload)
    print("test_crash_400k_uncompressed: HTTP %s" % resp.status_code)
    # Verify HTTP 200
    resp.raise_for_status()
    # Verify the response text contains a CrashID
    utils.verify_crashid(resp.text)


@scenario(0)
def test_crash_4mb_uncompressed():
    size = (4 * 1024 * 1024)
    raw_crash, dumps = utils.generate_sized_crashes(size)
    crash_payload = utils.assemble_crash_payload(raw_crash, dumps)
    payload, headers = utils.multipart_encode(crash_payload)

    if len(payload) != size:
        raise ValueError('payload size %s', len(payload))

    # POST the dump to Antenna
    resp = utils.post_crash(URL_SERVER, crash_payload)
    print("test_crash_4mb_uncompressed: HTTP %s" % resp.status_code)
    # Verify HTTP 200
    resp.raise_for_status()
    # Verify the response text contains a CrashID
    utils.verify_crashid(resp.text)


@scenario(0)
def test_crash_20mb_uncompressed():
    size = (20 * 1024 * 1024)
    raw_crash, dumps = utils.generate_sized_crashes(size)
    crash_payload = utils.assemble_crash_payload(raw_crash, dumps)
    payload, headers = utils.multipart_encode(crash_payload)

    if len(payload) != size:
        raise ValueError('payload size %s', len(payload))

    # POST the dump to Antenna
    resp = utils.post_crash(URL_SERVER, crash_payload)
    print("test_crash_20mb_uncompressed: HTTP %s" % resp.status_code)
    # Verify HTTP 200
    resp.raise_for_status()
    # Verify the response text contains a CrashID
    utils.verify_crashid(resp.text)


@scenario(0)
def test_crash_greater_than_20mb_uncompressed():
    size = (50 * 1024 * 1024)
    raw_crash, dumps = utils.generate_sized_crashes(size)
    crash_payload = utils.assemble_crash_payload(raw_crash, dumps)
    payload, headers = utils.multipart_encode(crash_payload)

    if len(payload) != size:
        raise ValueError('payload size %s', len(payload))

    # POST the dump to Antenna
    resp = utils.post_crash(URL_SERVER, crash_payload)
    print("test_crash_greater_than_20mb_uncompressed: HTTP %s" % resp.status_code)
    # Verify HTTP 413
    assert 413 == resp.status_code
