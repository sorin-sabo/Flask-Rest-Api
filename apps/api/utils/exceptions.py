"""
Authorization and NotFound related exceptions
"""


class AuthError(Exception):
    """
    Authorization exceptions class
    """
    def __init__(self, error, status_code):
        """
        Authorization exception constructor
        """
        super().__init__()
        self.error = error
        self.status_code = status_code


class NotFound(Exception):
    """
    *404* `Not Found`

    Raise if a resource does not exist and never existed.
    """

    def __init__(self, error):
        """
        Not Fount exception constructor
        """
        super().__init__()
        self.error = error
        self.status_code = 404
