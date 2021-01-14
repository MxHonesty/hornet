""" Created 14/01/2021 by Stelian Stoian.
    Module responsible for custom exceptions.
"""


class TorrentReadError(Exception):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return "Could not read file {}".format(self.filename)
