from endpoints import BaseEndpoint
from endpoints.enums import DEFAULT_API_VERSION, SECURE


class LoginEndpoint(BaseEndpoint):
    """
    Login endpoint.

    Args:
        host (str): Exabyte API hostname.
        port (int): Exabyte API port number.
        username (str): username.
        password (str): password.
        hashed (bool): whether a given password is SHA-256 hash. Defaults to False.
        version (str): Exabyte API version.
        secure (bool): whether to use secure http protocol (https vs http).
        kwargs (dict): a dictionary of HTTP session options.
            timeout (int): session timeout in seconds.

    Attributes:
        name (str): endpoint name.
        username (str): username.
        password (str): password.
    """

    def __init__(self, host, port, username, password, version=DEFAULT_API_VERSION, secure=SECURE, **kwargs):
        super(LoginEndpoint, self).__init__(host, port, version, secure, **kwargs)
        self.name = 'login'
        self.username = username
        self.password = password

    def login(self):
        """
        Logs in as a given user and generates an API token.

        Returns:
             dict
        """
        data = {'username': self.username, 'password': self.password}
        return self.request('POST', self.name, data=data)
