""" Created 09/01/2021 by Stelian Stoian.
    Test pipeline for the bencode subpackage.
"""

import unittest
from collections import OrderedDict

from src.bencode.decoder import Decoder


class TestDecoder(unittest.TestCase):
    def test_decode(self):
        """ Test for the decode method. """
        # Int starts with i and end with e.
        self.assertEqual(Decoder(b'i123e').decode(), 123)

        self.assertEqual(Decoder(b'12:Middle Earth').decode(), b'Middle Earth')

        # List starts with l<nr-elements> and ends with e. We have 2 e's here because of the int
        # terminator and the list indicator.
        self.assertEqual(Decoder(b'l4:spam4:salli123ee').decode(), [b'spam', b'sall', 123])

        self.assertEqual(Decoder(b'd5:salut6:nusunt3:eus4:eggse').decode(),
                         OrderedDict([(b'salut', b'nusunt'), (b'eus', b'eggs')]))


class TestEncoder(unittest.TestCase):
    def test_encode(self):
        """ Test for the encode method. """
        pass
