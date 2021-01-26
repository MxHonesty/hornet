""" Created 26/01/2021 by Stelian Stoian.
    This module implements the TrackerResponse class.
"""

import logging
import socket
from struct import unpack


class TrackerResponse:
    """ Class that manages Tracker response data.
        After a successful connection to the trackers announce URL.
    """
    def __init__(self, response: dict):
        self.response = response

    @property
    def failure(self):
        """ Returns the reason for failure expressed in the response.
            If no failure occurred, will return None.
        """
        if b'failure reason' in self.response:
            return self.response[b'failure reason'].decode('utf-8')
        return None

    @property
    def interval(self):
        """ Interval in seconds between tracker requests. """
        return self.response.get(b'interval', 0)

    @staticmethod
    def _decode_port(port):
        """ Converts 32-bit packed binary port to int. """
        return unpack(">H", port)[0]

    @property
    def peers(self):
        """ List of peers as (ip, port) tuples. """
        peers = self.response[b'peers']
        if isinstance(peers, list):
            logging.debug("Dictionary model peers")
            raise TypeError("not implemented")
        else:
            logging.debug("Binary model peers")
            peers = [peers[i:i+6] for i in range(0, len(peers), 6)]
            return [(socket.inet_ntoa(p[:4]), self._decode_port(p[4:])) for p in peers]
