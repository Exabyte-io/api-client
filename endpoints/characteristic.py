from endpoints import ExabyteBaseEndpoint


class ExabyteCharacteristicEndpoint(ExabyteBaseEndpoint):
    """
    Exabyte characteristic endpoint.

    Args:
        host (str): Exabyte API hostname.
        port (int): Exabyte API port number.
        user_id (str): user ID.
        auth_token (str): authentication token.

    Attributes:
        name (str): endpoint name.
        user_id (str): user ID.
        auth_token (str): authentication token.
        headers (dict): default HTTP headers.
    """

    def __init__(self, host, port, user_id, auth_token):
        self.name = 'characteristic'
        self.user_id = user_id
        self.auth_token = auth_token
        super(ExabyteCharacteristicEndpoint, self).__init__(host, port)
        self.headers = {'X-User-Id': self.user_id, 'X-Auth-Token': self.auth_token}

    def get_characteristics(self, page_index=0, page_size=20):
        """
        Returns a list of characteristics.

        Args:
            page_index (int): page index to return. Defaults to 0.
            page_size (int): page size. Defaults to 20.

        Returns:
            list[dict]
        """
        params = {'pageIndex': page_index, 'pageSize': page_size}
        return self.request('GET', self.name, params=params, headers=self.headers)

    def get_characteristic(self, cid):
        """
        Returns a characteristic with a given ID.

        Args:
            cid (str): characteristic ID.

        Returns:
             dict
        """
        return self.request('GET', '/'.join((self.name, cid)), headers=self.headers)

    def delete_characteristic(self, cid):
        """
        Deletes a given material.

        Args:
            cid (str): characteristic ID.
        """
        return self.request('DELETE', '/'.join((self.name, cid)), headers=self.headers)

    def update_characteristic(self, *args, **kwargs):
        pass

    def create_characteristic(self, *args, **kwargs):
        pass
