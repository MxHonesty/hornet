""" Created 09/01/2021 by Stelian Stoian.
    Implements the bencode encoder.
"""
from collections import OrderedDict

from src.bencode.indicators import TOKEN_END, TOKEN_INTEGER, TOKEN_DICT, TOKEN_LIST, TOKEN_STRING_SEPARATOR


class Encoder:
    """ Responsible for encoding a python object into the
        corresponding bencode. (int, str, list, ordered dict)
    """

    @staticmethod
    def encode(value_to_encode) -> bytes:
        """ The encode method encodes the object passed to the instance
            of the class to bytes type bencode.

            :param: value_to_encode The object that we want to encode. Can be
            int, str, list, OrderedDict.
        """
        if isinstance(value_to_encode, int):
            return Encoder._encode_int(value_to_encode)
        elif isinstance(value_to_encode, str):
            return Encoder._encode_string(value_to_encode)
        elif isinstance(value_to_encode, list):
            return Encoder._encode_list(value_to_encode)
        elif isinstance(value_to_encode, OrderedDict):
            return Encoder._encode_dict(value_to_encode)
        else:
            raise ValueError("Type {} of value_to_encode not supported".format(str(type(value_to_encode))))

    @staticmethod
    def _encode_int(value):
        """ Returns the bencode for the given int.

            Format of the int bencode is i<value>e. Ex: i123e.
            This is returned as bytes type.
        """
        res = TOKEN_INTEGER + Encoder._convert_int_to_byte_string(value) + TOKEN_END
        return res

    @staticmethod
    def _encode_string(value):
        """ Returns the bencode for given str.

            Format of the str bencode is <length>:<string>.
            This is returned as bytes type.
        """
        length = len(value)
        return Encoder._convert_int_to_byte_string(length) + TOKEN_STRING_SEPARATOR + bytes(value, encoding="utf8")

    @staticmethod
    def _encode_list(list_value):
        """ Returns the bencode for the given list. """
        res = b'l'
        new_elem = None
        for el in list_value:
            new_elem = Encoder._convert_base(el)
            res += new_elem
        return res + b'e'

    @staticmethod
    def _encode_dict(dict_value):
        """ Returns the bencode for the given dict. """
        res = b'd'
        for key in dict_value:
            new_key = Encoder._convert_base(key)
            new_object = Encoder._convert_base(dict_value[key])
            res += new_key + new_object
        return res + b'e'

    @staticmethod
    def _convert_base(value):
        """ Encode a basic value (int or string) to bencode.
            Utility function for converting basic types to their respective
            encoding.
            Raises ValueError if the wrong type is passed for value.
        """
        if isinstance(value, int):
            return Encoder._encode_int(value)
        elif isinstance(value, str):
            return Encoder._encode_string(value)
        else:
            raise ValueError("Value must be str or int but {} was passed".format(str(type(value))))

    @staticmethod
    def _convert_int_to_byte_string(value_to_convert):
        """ Convert an int value to a bytes string. """
        if not isinstance(value_to_convert, int):
            raise ValueError("value_to_convert must be int")
        cifre = []
        while value_to_convert:
            cifre.append(value_to_convert % 10)
            value_to_convert //= 10
        cifre.reverse()
        res = b''
        for el in cifre:
            if el == 1:
                res += b'1'
            elif el == 2:
                res += b'2'
            elif el == 3:
                res += b'3'
            elif el == 4:
                res += b'4'
            elif el == 5:
                res += b'5'
            elif el == 6:
                res += b'6'
            elif el == 7:
                res += b'7'
            elif el == 8:
                res += b'8'
            elif el == 9:
                res += b'9'
        return res
