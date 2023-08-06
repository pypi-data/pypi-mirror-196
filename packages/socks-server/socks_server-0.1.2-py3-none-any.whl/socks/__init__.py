__version__ = "0.1.2"

# Classes
from .classes import Socks
from .classes import Response
from .classes import ErrorResponse

# Functions
from .functions import renderTemplate

# ------------------ #
#  Stopping sockets  #
# ------------------ #

import gc
import socket
import atexit


def clearServers():
    from .classes import Server

    for obj in gc.get_objects():
        if isinstance(obj, Server):
            obj.sock.shutdown(socket.SHUT_RDWR)
            obj.sock.close()
            del obj

    print("Stopped server!")


atexit.register(clearServers)
