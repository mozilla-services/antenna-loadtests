import os

from ailoads.fmwk import scenario

import utils

URL_SERVER = os.getenv('URL_SERVER',
                       'https://antenna.stage.mozaws.net/submit')
DEBUG = False

if DEBUG:
    utils._log_everything()


# Meomoized generated payloads
CACHE = {}


def memoize(fun):
    """Decorates a function and memoizes it"""
    def _memoize(*args, **kwargs):
        key = repr((list(sorted(args)), list(sorted(kwargs.items()))))
        if key not in CACHE:
            ret = fun(*args, **kwargs)
            CACHE[key] = ret
        return CACHE[key]
    return _memoize


@memoize
def get_payload_and_headers(size, compressed=False):
    """Returns a payload and headers

    :arg size: the size in bytes the payload should be
    :arg compressed: whether or not to compress the payload

    :returns: ``(payload, headers)``

    """
    # Generate the payload and headers for a crash
    raw_crash, dumps = utils.generate_sized_crashes(size, compressed)

    # Convert the raw crash metadata and dumps into a single dict
    crash_payload = utils.assemble_crash_payload(raw_crash, dumps)

    # Convert the crash payload dict into a multipart/form-encode byte stream
    payload, headers = utils.multipart_encode(crash_payload)

    # If we should compress it, compress the byte stream and add relevant
    # header
    if compressed:
        payload = utils.compress(payload)
        headers['Content-Encoding'] = 'gzip'

    # Return payload and headers as a tuple
    return payload, headers


def run_test(name, size, compressed):
    payload, headers = get_payload_and_headers(size, compressed=compressed)
    resp = utils.post_crash(URL_SERVER, payload, headers, size)

    print('%s: HTTP %s' % (name, resp.status_code))
    # Verify HTTP 200
    resp.raise_for_status()
    # Verify the response text contains a CrashID
    utils.verify_crashid(resp.text)


@scenario(20)
def test_crash_100k_compressed():
    run_test('test_crash_100k_compressed', 100 * 1024, compressed=True)


@scenario(20)
def test_crash_150k_compressed():
    run_test('test_crash_150k_compressed', 150 * 1024, compressed=True)


@scenario(20)
def test_crash_400k_uncompressed():
    run_test('test_crash_400k_uncompressed', 400 * 1024, compressed=False)


@scenario(20)
def test_crash_4mb_uncompressed():
    run_test('test_crash_4mb_uncompressed', 4 * 1024 * 1024, compressed=False)


@scenario(20)
def test_crash_20mb_uncompressed():
    run_test('test_crash_20mb_uncompressed', 20 * 1024 * 1024,
             compressed=False)
