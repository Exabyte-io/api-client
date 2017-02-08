from endpoints import ExabyteBaseEndpoint


class ExabyteMaterialsEndpoint(ExabyteBaseEndpoint):
    """
    Exabyte materials endpoint.

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
        self.name = 'materials'
        self.user_id = user_id
        self.auth_token = auth_token
        super(ExabyteMaterialsEndpoint, self).__init__(host, port)
        self.headers = {'X-User-Id': self.user_id, 'X-Auth-Token': self.auth_token}

    def get_materials(self, include_chars=False, page_index=0, page_size=20):
        """
        Returns a list of materials.

        Args:
            include_chars (bool): whether to include material's characteristics.
            page_index (int): page index to return. Defaults to 0.
            page_size (int): page size. Defaults to 20.

        Returns:
            list[dict]
        """
        params = {'include_chars': include_chars, 'pageIndex': page_index, 'pageSize': page_size}
        return self.request('GET', self.name, params=params, headers=self.headers)

    def get_material(self, mid, include_chars=False):
        """
        Returns a material with a given ID.

        Args:
            mid (str): material ID.
            include_chars (bool): whether to include material's characteristics.

        Returns:
             dict
        """
        params = {'include_chars': include_chars}
        return self.request('GET', '/'.join((self.name, mid)), params=params, headers=self.headers)

    def get_materials_by_formula(self, formula, include_chars=False, page_index=0, page_size=20):
        """
        Returns a list of materials with a given formula.

        Args:
            formula (str): material's formula.
            include_chars (bool): whether to include material's characteristics.
            page_index (int): page index to return. Defaults to 0.
            page_size (int): page size. Defaults to 20.

        Returns:
            list[dict]
        """
        data = {'query': {'formula': formula}}
        params = {'include_chars': include_chars, 'pageIndex': page_index, 'pageSize': page_size}
        return self.request('POST', self.name, data=data, params=params, headers=self.headers)

    def delete_material(self, mid):
        """
        Deletes a given material.

        Args:
            mid (str): material ID.
        """
        return self.request('DELETE', '/'.join((self.name, mid)), headers=self.headers)

    def update_material(self, material):
        pass

    def create_material(self, material):
        return self.request('POST', self.name, data=material, headers=self.headers)
