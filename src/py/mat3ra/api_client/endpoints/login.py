from . import BaseEndpoint
from .enums import DEFAULT_API_VERSION, SECURE


class LoginEndpoint(BaseEndpoint):
    """
    Login endpoint.

    Args:
        host (str): API hostname.
        port (int): API port number.
        username (str): username.
        password (str): password.
        version (str): API version.
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
        self.name = "login"
        self.username = username
        self.password = password

    def login(self):
        """
        Logs in as a given user and generates an API token.

        Returns:
             dict
        """
        data = {"username": self.username, "password": self.password}
        return self.request("POST", self.name, data=data)

    @staticmethod
    def get_endpoint_options(host, port, username, password, version=DEFAULT_API_VERSION, secure=SECURE):
        """
        Logs in with given parameters and returns options to use for further calls to the RESTful API.

        Args:
            host (str): API hostname.
            port (int): API port number.
            username (str): username.
            password (str): password.
            version (str): API version.
            secure (bool): whether to use secure http protocol (https vs http).

        Returns:
            dict
        """
        endpoint = LoginEndpoint(host, port, username, password, version, secure)
        response = endpoint.login()
        return {
            "host": host,
            "port": port,
            "secure": secure,
            "version": version,
            "auth_token": response["X-Auth-Token"],
            "account_id": response["X-Account-Id"],
        }
