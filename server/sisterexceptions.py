class UsernameException(Exception):
    '''
    The Exception raised when the server is having problem with usernames.
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class TokenException(Exception):
    '''
    The Exception raised when the server is having problem with tokens.
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class OfferException(Exception):
    '''
    The Exception raised when the server is having problem with offers.
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class MixtureException(Exception):
    '''
    The Exception raised when the server is having problem with mixture.
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class IndexItemException(Exception):
    '''
    The Exception raised when the server is having problem with item's index.
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value