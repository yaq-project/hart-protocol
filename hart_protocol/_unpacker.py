__all__ = ["Unpacker"]

import asyncio
from collections import namedtuple
import io
import struct
import warnings

from ._parsing import parse
from . import tools


class Unpacker:
    """
    Create an Unpacker to decode a byte stream into HART protocol messages.

    The ``file_like`` parameter should be an object which data can be sourced from.
    It should support the ``read()`` method.

    The ``on_error`` parameter selects the action to take if invalid data is detected.
    If set to ``"continue"`` (the default), bytes will be discarded if the byte sequence
    does not appear to be a valid message.
    If set to ``"warn"``, the behaviour is identical, but a warning message will be emitted.
    To instead immediately abort the stream decoding and raise a ``RuntimeError``, set to
    ``"raise"``.

    :param file_like: A file-like object which data can be `read()` from.
    :param on_error: Action to take if invalid data is detected.
    """

    def __init__(self, file_like=None, on_error="continue"):
        if file_like is None:
            self._file = io.BytesIO()
        else:
            self._file = file_like
        self.buf = b""
        self.on_error = on_error

    def __iter__(self):
        return self

    def _decoding_error(self, message="Error decoding message from buffer."):
        """
        Take appropriate action if parsing of data stream fails.

        :param message: Warning or error message string.
        """
        if self.on_error == "raise":
            raise RuntimeError(message)
        if self.on_error == "warn":
            warnings.warn(message)
        # Discard first byte of buffer, it might decode better now...
        self.buf = self.buf[1:]

    def __next__(self):
        # must work with at least two bytes to start with
        while len(self.buf) < 2:
            self.buf += self._file.read(1)
        # keep reading until we find a minimum preamble
        while self.buf[:2] != b"\xFF\xFF":
            self.buf += self._file.read(1)
            self._decoding_error("Head of buffer not recognized as valid preamble")
        # now we are within the preamble, seek forward for start charachter
        while True:
            if len(self.buf) < 2:
                self.buf += self._file.read(1)
            if self.buf[0] == 0xFF:
                self.buf = self.buf[1:]
            elif self.buf[0] in [0x06, 0x86]:
                break
            else:
                self._decoding_error("Preamble did not end with start charachter.")
                raise StopIteration
        # now the head of our buffer is the start charachter
        # we will read all the way through status
        if self.buf[0] & 0x80:
            l = 10
        else:
            l = 6
        while len(self.buf) < l:
            self.buf += self._file.read(1)
        # now we can use the bytecount to read through the data and checksum
        bytecount = self.buf[l - 3]
        response_length = l + bytecount - 1
        while len(self.buf) < response_length:
            self.buf += self._file.read(1)
        # checksum
        checksum = int.from_bytes(tools.calculate_checksum(self.buf[: response_length - 1]), "big")
        if checksum != self.buf[response_length - 1]:
            self._decoding_error("Invalid checksum.")
            raise StopIteration
        # parse
        response = self.buf[: response_length + 1]
        dict_ = parse(response)
        # clear buffer
        if len(self.buf) == response_length:
            self.buf = b""
        else:
            self.buf = self.buf[response_length + 1 :]
        # return
        return namedtuple(dict_["command_name"], dict_.keys())(**dict_)

    def __aiter__(self):
        return self

    async def __anext__(self):
        while True:
            try:
                return next(self)
            except StopIteration:
                await asyncio.sleep(0.001)

    def feed(self, data: bytes):
        """
        Add byte data to the input stream.

        The input stream must support random access, if it does not, must be fed externally
        (e.g. serial port data).

        :param data: Byte array containing data to add.
        """
        pos = self._file.tell()
        self._file.seek(0, 2)
        self._file.write(data)
        self._file.seek(pos)
