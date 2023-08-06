import os
import socket

import urllib.parse


def parseKeyValue(string):
    """
    Parse a string of the form or url parameter key=value into a dictionary.
    """
    data = {}
    for param in string.split("&"):
        data[urllib.parse.unquote(param.split("=")[0])] = urllib.parse.unquote(
            param.split("=")[1]
        )

    return data


def getAppRunDir():
    """
    Get the parent directory of the current file.
    """
    return os.getcwd()


def getLocalIp():
    # Get ip, source: https://stackoverflow.com/a/1267524
    return (
        (
            [
                ip
                for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                if not ip.startswith("127.")
            ]
            or [
                [
                    (s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())
                    for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
                ][0][1]
            ]
        )
        + [None]
    )[0]
