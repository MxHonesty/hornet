""" Created 09/01/2021 by Stelian Stoian.
    Implements the bencode decoder.
"""
from collections import OrderedDict

from src.bencode.indicators import TOKEN_INTEGER, TOKEN_DICT, TOKEN_STRING_SEPARATOR, TOKEN_END, TOKEN_LIST


class Decoding:
    """ Responsible for decoding a bencoded sequence of bytes.
        Raises TypeError if data is not bytes.
    """
    def __init__(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError("Argument data must be of type bytes")
        self._data = data
        self._index = 0

    def decode(self):
        """ Decode the data and return the python object. """
        current_char = self._next_character()
        if current_char is None:
            raise EOFError("Unexpected EOF")
        if current_char == TOKEN_INTEGER:
            self._skip_character()
            return self._decode_int()
        elif current_char == TOKEN_LIST:
            self._skip_character()
            return self._decode_list()
        elif current_char == TOKEN_DICT:
            self._skip_character()
            return self._decode_dict()
        elif current_char in b'0123456789':
            return self._decode_string()
        else:
            raise RuntimeError("Unsupported token found")

    def _next_character(self):
        """ Return the next character from the bencode data or None if nothing left. """
        if self._index + 1 >= len(self._data):
            return None
        return self._data[self._index:self._index + 1]

    def _skip_character(self):
        """ Move the current character to the right by one. """
        self._index += 1

    def _read(self, length: int) -> bytes:
        """ Read the length number of bytes from data starting at _index. """
        if self._index + length > len(self._data):
            raise IndexError("Cannot read {} bytes from current position {}".format(str(length), str(self._index)))
        res = self._data[self._index:self._index + length]
        self._index += length
        return res

    def _read_until(self, token: bytes) -> bytes:
        """ Read the data until de token is found starting from _index.
            Raises RuntimeError if the token is not found.
        """
        try:
            token_position = self._data.index(token, self._index)  # Index where token is found first after _index.
            result = self._data[self._index:token_position]
            self._index = token_position + 1
            return result
        except ValueError:
            raise RuntimeError("Not able to find the {} token".format(str(token)))

    def _decode_int(self):
        """ Decode the current data as int. """
        return int(self._read_until(TOKEN_END))

    def _decode_list(self):
        """ Decode the current data as a list. """
        resulting_list = []
        while self._index < len(self._data) - 1:
            resulting_list.append(self.decode())
        return resulting_list

    def _decode_dict(self):
        """ Decode the current data as a dict. """
        resulting_dict = OrderedDict()
        while self._index < len(self._data) - 1:
            key_object = self.decode()
            value_object = self.decode()
            resulting_dict[key_object] = value_object
        return resulting_dict

    def _decode_string(self):
        """ Decode the current data as a string. """
        length = int(self._read_until(TOKEN_STRING_SEPARATOR))
        return self._read(length)


class Decoder:
    """ Wrapper class for the Decoding functionality. """
    @staticmethod
    def decode(bencode: bytes):
        """ Function that decodes the bencode into corresponding python object.
            Input is bencode to be decoded as bytes.
            Output can be list, OrderedDict, int, str.
        """
        return Decoding(bencode).decode()
