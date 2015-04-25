import calendar
import time


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