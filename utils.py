from email.header import Header
import io
import gzip
import logging
import random
import string
import uuid

import requests
import six


def _log_everything():
    # Set up all the debug logging for grossest possible output
    from http.client import HTTPConnection
    HTTPConnection.debuglevel = 1

    logging.getLogger('requests').setLevel(logging.DEBUG)
    logging.getLogger('requests.packages.urllib3').setLevel(logging.DEBUG)


def print_debug(resp):
    print(resp.status_code)
    print(resp.headers)
    print(resp.text)


def assemble_crash_payload(raw_crash, dumps):
    crash_data = dict(raw_crash)

    if dumps:
        for name, contents in dumps.items():
            if isinstance(contents, six.text_type):
                contents = contents.encode('utf-8')
            elif isinstance(contents, six.binary_type):
                contents = contents
            else:
                contents = six.text_type(contents).encode('utf-8')
            crash_data[name] = ('fakecrash.dump', io.BytesIO(contents))
    return crash_data


def compress(multipart):
    """Takes a multi-part/form-data payload and compresses it

    :arg multipart: a bytes object representing a multi-part/form-data

    :returns: bytes compressed

    """
    bio = io.BytesIO()
    g = gzip.GzipFile(fileobj=bio, mode='w')
    g.write(multipart)
    g.close()
    return bio.getbuffer()


def multipart_encode(raw_crash, boundary=None):
    """Takes a raw_crash as a Python dict and converts to a multipart/form-data

    Here's an example ``raw_crash``::

        {
            'ProductName': 'Test',
            'Version': '1.0',
            'upload_file_minidump': ('fakecrash.dump', io.BytesIO(b'abcd1234'))
        }

    You can also pass in file pointers for files::

        {
            'ProductName': 'Test',
            'Version': '1.0',
            'upload_file_minidump': ('fakecrash.dump', open('crash.dmp', 'rb'))
        }


    This returns a tuple of two things:

    1. a ``bytes`` object with the HTTP POST payload
    2. a dict of headers with ``Content-Type`` and ``Content-Length`` in it


    :arg params: Python dict of name -> value pairs. Values must be either
         strings or a tuple of (filename, file-like objects with ``.read()``).

    :arg boundary: The MIME boundary string to use. Otherwise this will be
        generated.

    :returns: tuple of (bytes, headers dict)

    """
    if boundary is None:
        boundary = '0a6e8e03c28e4e37abb57837f9ebf405'

    output = io.BytesIO()
    headers = {
        'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
    }

    for key, val in sorted(raw_crash.items()):
        block = [
            '--%s' % boundary
        ]

        if isinstance(val, (float, int, str)):
            block.append('Content-Disposition: form-data; name="%s"' % Header(key).encode())
            block.append('Content-Type: text/plain; charset=utf-8')
        elif isinstance(val, tuple):
            block.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (
                (Header(key).encode(), Header(val[0]).encode())))
            block.append('Content-Type: application/octet-stream')
        else:
            print('Skipping %r %r' % key)
            continue

        block.append('')
        block.append('')

        output.write('\r\n'.join(block).encode('utf-8'))

        if isinstance(val, str):
            output.write(val.encode('utf-8'))
        elif isinstance(val, (float, int)):
            output.write(str(val).encode('utf-8'))
        else:
            output.write(val[1].read())

        output.write(b'\r\n')

    # Add end boundary and convert to bytes.
    output.write(('--%s--\r\n' % boundary).encode('utf-8'))
    output = output.getvalue()

    headers['Content-Length'] = str(len(output))

    return output, headers


def post_crash(url, payload, headers, size, compressed=False):
    """Posts a crash to specified url

    .. Note:: This is not full-featured. It's for testing purposes only.

    :arg str url: The url to post to.
    :arg dict crash_payload: The raw crash and dumps as a single thing.
    :arg int size: The expected payload size
    :arg bool compressed: Whether or not to post a compressed payload.

    :returns: The requests Response instance.

    """
    assert len(payload) == size, (
        'Payload is not the right size! %s vs. %s' % (len(payload), size)
    )

    if compressed:
        payload = compress(payload)
        headers['Content-Encoding'] = 'gzip'

    return requests.post(
        url,
        headers=headers,
        data=payload,
        allow_redirects=True
    )


def generate(metadata=None, dumps=None):
    """Returns raw_crash, dumps"""
    raw_crash = {
        'ProductName': 'Firefox',
        'Version': '1',
    }
    if dumps is None:
        dumps = {
            'upload_file_minidump': b'abcd1234'
        }

    if metadata is not None:
        raw_crash.update(metadata)

    return raw_crash, dumps


def generate_sized_crashes(size, compressed=False):
    """Generates a payload that's of the specified size

    For compressed payloads, we want the compressed payloed to be of the
    specified size after compressing.

    This is a brute-force algorithm to figure that out.

    """
    raw_crash, dumps = generate()

    dumps['upload_file_minidump'] = ''

    crash_payload = assemble_crash_payload(raw_crash, dumps)
    payload, headers = multipart_encode(crash_payload)
    base_size = len(payload)

    # Create a "dump file" which is really just a bunch of random
    # characters such that the entire payload is equal to size
    dumps['upload_file_minidump'] = 'a' * (size - base_size)

    if not compressed:
        # This is the easy case, so we just do it and move on
        return raw_crash, dumps

    # This is the hard case. We need to generate a payload that when compressed
    # is of the right size. So we loop.
    def get_char():
        return random.choice(string.ascii_letters)

    compressed_size = len(compress(payload))
    while compressed_size != size:
        if compressed_size > size:
            # If we're over, then drop the first 10 characters
            dumps['upload_file_minidump'] = dumps['upload_file_minidump'][10:]

        else:
            # If we're under, then add a bunch of characters in a way that
            # tries to "bisect" the distance we still need to cover because we
            # want to get on with living our lives
            num = int((size - compressed_size) / 2) + 1
            dumps['upload_file_minidump'] += ''.join(
                [get_char() for i in range(num)]
            )

        crash_payload = assemble_crash_payload(raw_crash, dumps)
        payload, headers = multipart_encode(crash_payload)
        compressed_size = len(compress(payload))

    return raw_crash, dumps


def verify_crashid(resp_text):
    # Verify the response text begins with CrashID
    assert resp_text.startswith("CrashID=")
    # Verify the returned CrashID begins with bp-
    crash_id = resp_text.split("CrashID=")[1]
    assert crash_id.startswith("bp-")
    # Verify the returned crash_id has a character length greater than "bp-"
    assert 3 < len(crash_id)
