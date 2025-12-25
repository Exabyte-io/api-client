from . import BaseEndpoint
from .enums import DEFAULT_API_VERSION, SECURE


class LogoutEndpoint(BaseEndpoint):
    """
    Logout endpoint.

    Args:
        host (str): API hostname.
        port (int): API port number.
        account_id (str): account ID.
        auth_token (str): authentication token.
        version (str): API version.
        secure (bool): whether to use secure http protocol (https vs http).
        kwargs (dict): a dictionary of HTTP session options.
            timeout (int): session timeout in seconds.

    Attributes:
        name (str): endpoint name.
        headers (dict): default HTTP headers.
    """

    def __init__(self, host, port, account_id, auth_token, version=DEFAULT_API_VERSION, secure=SECURE, **kwargs):
        super(LogoutEndpoint, self).__init__(host, port, version, secure, **kwargs)
        self.name = "logout"
        self.headers = self.get_headers(account_id, auth_token)

    def logout(self):
        """
        Deletes current API token.
        """
        return self.request("POST", self.name, headers=self.headers)
