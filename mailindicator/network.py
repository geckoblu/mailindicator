"""-"""
import socket

import mailindicator.logging as logging


def network_available():
    """Check if a network connection is available"""
    try:
        # connect to the host -- tells us if the host is actually reachable
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        pass
    logging.info("No network available.")
    return False
