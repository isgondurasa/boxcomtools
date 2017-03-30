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
