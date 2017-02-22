import os
import sys; sys.path.append('.')

from molotov import scenario

import utils


url_server = os.getenv('URL_SERVER',
                       'https://antenna-loadtest.stage.mozaws.net')
URL_SERVER = '{0}/submit'.format(url_server)


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
def get_payload_and_headers(size, dump_names=None, compressed=False):
    """Returns a payload and headers ready for posting

    :arg size: the size in bytes the payload should be
    :arg dump_names: list of dumps to include; default is
        ``['upload_file_minidump']``
    :arg compressed: whether or not to compress the payload

    :returns: ``(payload, headers)``

    """
    if not dump_names:
        dump_names = ['upload_file_minidump']

    # Generate the payload and headers for a crash
    raw_crash, dumps = utils.generate_sized_crashes(
        size, dump_names=dump_names, compressed=compressed
    )

    # Make sure we have the specified dumps
    assert list(sorted(dumps.keys())) == list(sorted(dump_names)), (
        'Dumps are missing. There is a bug in the test code. %s vs. %s' % (
            dumps.keys(), dump_names
        )
    )

    # Convert the raw crash metadata and dumps into a single dict
    crash_payload = utils.assemble_crash_payload(raw_crash, dumps)

    # Convert the crash payload dict into a multipart/form-encode byte stream
    payload, headers = utils.multipart_encode(crash_payload)

    # If we should compress it, compress the byte stream and add relevant
    # header
    if compressed:
        payload = utils.compress(payload)
        headers['Content-Encoding'] = 'gzip'
        headers['Content-Length'] = str(len(payload))

    # Make sure the final payload size is correct
    assert len(payload) == size, (
        'Payload is not the right size! %s vs. %s' % (len(payload), size)
    )

    # Return payload and headers as a tuple
    return payload, headers


async def run_test(name, session, size, dump_names=None, compressed=False):
    payload, headers = get_payload_and_headers(size, dump_names=dump_names, compressed=compressed)
    async with session.post(URL_SERVER, headers=headers, data=payload,
                            compress=False, allow_redirects=True) as resp:
        # Verify HTTP 200
        assert resp.status == 200
        # Verify the response text contains a CrashID
        utils.verify_crashid(await resp.text())


@scenario(0)
async def _test_crash_100k_compressed(session):
    await run_test('test_crash_100k_compressed', session, 100 * 1024, compressed=True)


@scenario(10)
async def _test_crash_150k_compressed(session):
    await run_test('test_crash_150k_compressed', session, 150 * 1024, compressed=True)


@scenario(60)
async def _test_crash_400k_uncompressed(session):
    await run_test('test_crash_400k_uncompressed', session, 400 * 1024, compressed=False)


@scenario(5)
async def _test_crash_1_5mb_uncompressed(session):
    await run_test('test_crash_1_5mb_uncompressed', session, int(1.5 * 1024 * 1024), compressed=False)


@scenario(0)
async def _test_crash_4mb_uncompressed(session):
    await run_test('test_crash_4mb_uncompressed', session, 4 * 1024 * 1024, compressed=False)


@scenario(0)
async def _test_crash_20mb_uncompressed(session):
    await run_test('test_crash_20mb_uncompressed', session, 20 * 1024 * 1024, compressed=False)


@scenario(25)
async def _test_crash_400k_uncompressed_multiple_dumps(session):
    await run_test('test_crash_400k_uncompressed_multiple_dumps', session, 400 * 1024,
             dump_names=[
                 'upload_file_minidump',
                 'upload_file_minidump_browser',
                 'upload_file_minidump_flash1',
                 'upload_file_minidump_flash2',
             ],
             compressed=False)
