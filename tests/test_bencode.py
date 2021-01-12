""" Created 09/01/2021 by Stelian Stoian.
    Test pipeline for the bencode subpackage.
"""

import unittest
from collections import OrderedDict

from src.bencode.decoder import Decoder
from src.bencode.encoder import Encoder


class TestDecoder(unittest.TestCase):
    def test_decode(self):
        """ Test for the decode method. """
        # Int starts with i and end with e.
        self.assertEqual(Decoder().decode(b'i123e'), 123)

        self.assertEqual(Decoder().decode(b'12:Middle Earth'), b'Middle Earth')

        # List starts with l<nr-elements> and ends with e. We have 2 e's here because of the int
        # terminator and the list indicator.
        self.assertEqual(Decoder().decode(b'l4:spam4:salli123ee'), [b'spam', b'sall', 123])

        self.assertEqual(Decoder().decode(b'd5:salut6:nusunt3:eus4:eggse'),
                         OrderedDict([(b'salut', b'nusunt'), (b'eus', b'eggs')]))


class TestEncoder(unittest.TestCase):
    def test_encode(self):
        """ Test for the encode method. """
        int_test = 123
        string_test = "salut"
        list_test = [123, 321, "salut"]
        dict_test = OrderedDict([("salut", "nusunt"), ("eus", "eggs")])
        dict_test2 = OrderedDict([(123, "salut"), (132, 32)])

        self.assertEqual(Encoder.encode(int_test), b'i123e')
        self.assertEqual(Encoder.encode(string_test), b'5:salut')
        self.assertEqual(Encoder.encode(list_test), b'li123ei321e5:salute')
        self.assertEqual(Encoder.encode(dict_test), b'd5:salut6:nusunt3:eus4:eggse')
        self.assertEqual(Encoder.encode())
