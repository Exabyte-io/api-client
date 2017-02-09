from endpoints import ExabyteBaseEndpoint


class ExabyteMaterialsBankEndpoint(ExabyteBaseEndpoint):
    """
    Exabyte materials-bank endpoint.

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
        self.name = 'materials-bank'
        self.user_id = user_id
        self.auth_token = auth_token
        super(ExabyteMaterialsBankEndpoint, self).__init__(host, port, version=version, secure=secure, **kwargs)
        self.headers = {'X-User-Id': self.user_id, 'X-Auth-Token': self.auth_token}

    def get_materials(self, params=None):
        """
        Returns a list of materials from materials-bank.

        Args:
            params (dict): a dictionary of parameters passed to materials endpoint.
                pageSize (int): page size. Defaults to 20.
                pageIndex (int): page index to return. Defaults to 0.
                mongoQuery (dict): mongo query to filter the results.
                includeCharacteristics (bool): whether to include material's characteristics.

        Returns:
            list[dict]
        """
        return self.request('GET', self.name, params=params, headers=self.headers)

    def get_material(self, mid, params=None):
        """
        Returns a material with a given ID from materials-bank.

        Args:
            mid (str): material ID.
            params (dict): a dictionary of parameters passed to materials endpoint.
                includeCharacteristics (bool): whether to include material's characteristics.

        Returns:
             dict: material.
        """
        return self.request('GET', '/'.join((self.name, mid)), params=params, headers=self.headers)

    def get_materials_by_formula(self, formula, params=None):
        """
        Returns a list of materials with a given formula from materials-bank.

        Args:
            formula (str): material's formula.
            params (dict): a dictionary of parameters passed to materials endpoint.
                pageSize (int): page size. Defaults to 20.
                pageIndex (int): page index to return. Defaults to 0.
                includeCharacteristics (bool): whether to include material's characteristics.

        Returns:
            list[dict]
        """
        query = {'mongoQuery': {'formula': formula}}
        params = params.update(query) if params else query
        return self.request('GET', self.name, params=params, headers=self.headers)

    def delete_material(self, mid):
        """
        Deletes a given material from materials-bank.

        Args:
            mid (str): material ID.
        """
        return self.request('DELETE', '/'.join((self.name, mid)), headers=self.headers)

    def update_material(self, mid, kwargs):
        """
        Updates a material inside materials-bank with given key-values in kwargs.

        Args:
            mid (str): material ID.
            kwargs (dict): a dictionary of key-values to update.

        Returns:
             dict: updated material.
        """
        return self.request('PATCH', '/'.join((self.name, mid)), data=kwargs, headers=self.headers)

    def create_material(self, material):
        """
        Creates a new material inside materials-bank.

        Args:
            material (dict): material object.

        Returns:
             dict: new material.
        """
        return self.request('POST', self.name, data=material, headers=self.headers)
