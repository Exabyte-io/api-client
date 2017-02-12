import json

from endpoints import ExabyteBaseEndpoint


class ExabyteCharacteristicEndpoint(ExabyteBaseEndpoint):
    """
    Exabyte characteristic endpoint.

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
        self.name = 'characteristic'
        self.user_id = user_id
        self.auth_token = auth_token
        super(ExabyteCharacteristicEndpoint, self).__init__(host, port, version=version, secure=secure, **kwargs)
        self.headers = {'X-User-Id': self.user_id, 'X-Auth-Token': self.auth_token}

    def get_characteristics(self, params=None):
        """
        Returns a list of characteristics.

        Args:
            params (dict): a dictionary of parameters passed to materials endpoint.
                pageSize (int): page size. Defaults to 20.
                pageIndex (int): page index to return. Defaults to 0.
                query (dict): mongo query to filter the results.

        Returns:
            list[dict]
        """
        return self.request('GET', self.name, params=params, headers=self.headers)

    def get_characteristic(self, cid):
        """
        Returns a characteristic with a given ID.

        Args:
            cid (str): characteristic ID.

        Returns:
             dict: characteristic.
        """
        return self.request('GET', '/'.join((self.name, cid)), headers=self.headers)

    def delete_characteristic(self, cid):
        """
        Deletes a given material.

        Args:
            cid (str): characteristic ID.
        """
        return self.request('DELETE', '/'.join((self.name, cid)), headers=self.headers)

    def update_characteristic(self, cid, kwargs):
        """
        Updates a characteristic with given key-values in kwargs.

        Args:
            cid (str): characteristic ID.
            kwargs (dict): a dictionary of key-values to update.

        Returns:
             dict: updated characteristic.
        """
        headers = dict([('Content-Type', 'application/json')])
        headers.update(self.headers)
        return self.request('PATCH', '/'.join((self.name, cid)), data=json.dumps(kwargs), headers=headers)

    def create_characteristic(self, characteristic):
        """
        Creates a new material.

        Args:
            characteristic (dict): characteristic object.

        Returns:
             dict: new characteristic.
        """
        headers = dict([('Content-Type', 'application/json')])
        headers.update(self.headers)
        return self.request('POST', self.name, data=json.dumps(characteristic), headers=headers)
