from endpoints import ExabyteBaseEndpoint


class ExabyteLogoutEndpoint(ExabyteBaseEndpoint):
    """
    Exabyte logout endpoint.

    Args:
        host (str): Exabyte API hostname.
        port (int): Exabyte API port number.
        user_id (str): user ID.
        auth_token (str): authentication token.
        version (str): Exabyte API version. Defaults to v1.
        secure (bool): whether to use secure http protocol (https vs http). Defaults to True.
        kwargs (dict): a dictionary of HTTP session options.
            timeout (int): session timeout in seconds.

    Attributes:
        name (str): endpoint name.
        user_id (str): user ID.
        auth_token (str): authentication token.
        headers (dict): default HTTP headers.
    """

    def __init__(self, host, port, user_id, auth_token, version='v1', secure=True, **kwargs):
        self.name = 'logout'
        self.user_id = user_id
        self.auth_token = auth_token
        super(ExabyteLogoutEndpoint, self).__init__(host, port, version=version, secure=secure, **kwargs)
        self.headers = {'X-User-Id': self.user_id, 'X-Auth-Token': self.auth_token}

    def logout(self):
        """
        Calls Exabyte logout endpoint to invalidate authentication token.
        """
        return self.request('POST', self.name, headers=self.headers)
