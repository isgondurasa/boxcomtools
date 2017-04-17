# exceptions.py    

class NoClientID(Exception):
    """User doesn't pass any client_id"""


class NoClientSecret(Exception):
    """User doesn't pass any client_secret"""


class NoAuthCodeDefined(Exception):
    pass


class NoAccessTokenException(Exception):
    pass


class NoAccessTokenDefined(Exception):
    pass

class HTTPError(Exception):
    def __init__(self, status, reason):
        self._status = status
        self._reason = reason

    def __str__(self):
        return "Error. Status {}: {}".format(self._status, self._reason)
    
