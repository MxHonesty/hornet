""" Created 14/01/2021 by Stelian Stoian.
    Test pipeline for the Torrent module.
"""

import unittest

from src.errors import TorrentReadError
from src.torrent import Torrent


class TesTorrent(unittest.TestCase):

    def setUp(self):
        self.tor = Torrent("test.torrent")

    def test_properties(self):
        property_error = "Torrent metadata read error"

        filename = "ubuntu-20.04.1-desktop-amd64.iso"
        file_length = 2785017856
        announce = "https://torrent.ubuntu.com/announce"
        hash_info = b'\x1eH\xa6T4\x8cQ\x9b\x11\x8d\x0b}\x0ep\xed\xf2\xfb\x93\n\x90'
        self.assertEqual(self.tor.output_file, filename, msg=property_error)
        self.assertEqual(self.tor.total_size, file_length, msg=property_error)
        self.assertEqual(self.tor.announce, announce, msg=property_error)
        self.assertEqual(self.tor.info_hash, hash_info, msg=property_error)

    def test_read(self):
        self.assertRaises(TorrentReadError, lambda: Torrent("nonexistent.torrent"), msg="Check if error raised")
