from endpoints import ExabyteBaseEndpoint


class ExabyteLoginEndpoint(ExabyteBaseEndpoint):
    """
    Exabyte login endpoint.

    Args:
        host (str): Exabyte API hostname.
        port (int): Exabyte API port number.
        username (str): username.
        password (str): password.
        hashed (bool): whether a given password is SHA-256 hash. Defaults to False.

    Attributes:
        name (str): endpoint name.
        username (str): username.
        password (str): password.
        hashed (bool): whether a given password is SHA-256 hash. Defaults to False.
    """

    def __init__(self, host, port, username, password, hashed=False):
        self.name = 'login'
        self.username = username
        self.password = password
        self.hashed = hashed
        super(ExabyteLoginEndpoint, self).__init__(host, port)

    def login(self):
        """
        Calls Exabyte login endpoint to retrieve X-Auth-Token and X-User-Id.

        Returns:
             dict: {'user_id': user_id, 'auth_token': auth_token}
        """
        data = {'username': self.username, 'password': self.password}
        if self.hashed:
            data.update({'hashed': 'true'})
        response = self.request('POST', self.name, data=data)
        return {'user_id': response['data']['userId'], 'auth_token': response['data']['authToken']}
