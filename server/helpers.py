import calendar
import json
import time
import socket


def containsValidJSON(data):
    """
    Check wether data contains a valid JSON or not.
    This function can't handle JSON with curly braces elements.

    :param data: string
    :return: boolean
    """

    balance = 0
    found = False

    for c in data:
        if c == '{':
            if not found:
                found = True
            balance += 1

        elif c == '}':
            if found:
                balance -= 1
                if balance == 0:
                    return True

    return False


def getCurrentTime():
    """
    Get the current Unix Time.

    :return: integer, unix time
    """

    return calendar.timegm(time.gmtime())


def mappingIndexItemToName(index):
    """
    Return the itemCode from itemID
    :param index: int
    :return: string, itemCode
    """

    if index == 0:
        return 'R11'
    elif index == 1:
        return 'R12'
    elif index == 2:
        return 'R13'
    elif index == 3:
        return 'R14'
    elif index == 4:
        return 'R21'
    elif index == 5:
        return 'R22'
    elif index == 6:
        return 'R23'
    elif index == 7:
        return 'R31'
    elif index == 8:
        return 'R32'
    elif index == 9:
        return 'R41'


def mappingNameItemToIndex(name):
    """
    Return the itemID from the itemCode
    :param name: string
    :return: int
    """

    if name == 'R11':
        return 0
    elif name == 'R12':
        return 1
    elif name == 'R13':
        return 2
    elif name == 'R14':
        return 3
    elif name == 'R21':
        return 4
    elif name == 'R22':
        return 5
    elif name == 'R23':
        return 6
    elif name == 'R31':
        return 7
    elif name == 'R32':
        return 8
    elif name == 'R41':
        return 9

def sendJSON(address, toSend, timeout=None):
    """
    Send JSON to other host and receive a reply.

    :param: address (ip: string, port: int)
    :param: toSend dictionary representing the JSON
    :return: dictionary representing the JSON of the response
    """

    # setup connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect(address)

    # send and receive
    s.sendall(json.dumps(toSend))

    everything = ''
    while True:
        data = s.recv(4096)
        everything += data
        if containsValidJSON(everything):
            break

    return json.loads(everything)