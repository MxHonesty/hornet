""" Created 23/01/2021 by Stelian Stoian.
    This module implements the peer_id generator.
"""

import random


def generate_peer_id():
    """ Generates a Azureus-style peer_id for the client.

        Format -<ID><version>-<12 digit code>
    """
    return '-HR0001-' + ''.join([str(random.randint(0, 9)) for i in range(12)])
