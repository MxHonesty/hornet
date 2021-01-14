""" Created 09/01/2021 by Stelian Stoian.
    This module implements the Torrent class.
"""
from hashlib import sha1

from bencode.decoder import Decoder
from bencode.encoder import Encoder


class TorrentFile:
    """ Class representing a torrent file. """
    def __init__(self, name, length):
        self.name = name
        self.length = length


class Torrent:
    """ Class representing the torrent meta-data from within the .torrent file. """
    def __init__(self, filename):
        self.filename = filename
        self.files = []

        with open(self.filename, 'rb') as f:
            information = f.read()
            self.data = Decoder.decode(information)
            info = Encoder.encode(self.data[b'info'])
            self.info_hash = sha1(info).digest()
            self._identify_files()  # Identify files in meta-data.

    def _identify_files(self):
        self.files.append(TorrentFile(self.data[b'info'][b'name'].decode('utf-8'),
                          self.data[b'info'][b'length']))

    @property
    def total_size(self) -> int:
        """ Returns the total size in bytes for """
        return self.files[0].length

    @property
    def announce(self) -> str:
        """ Returns the announce URL to the tracker. """
        return self.data[b'announce'].decode('utf-8')

    @property
    def output_file(self):
        return self.data[b'info'][b'name'].decode('utf-8')

    def __str__(self):
        return 'Filename: {}\n'\
            'File length: {}\n' \
            'Announce URL: {}\n' \
            'Hash: {}'.format(self.data[b'info'][b'name'],
                              self.data[b'info'][b'length'],
                              self.data[b'announce'],
                              self.info_hash)


tor = Torrent("test.torrent")
