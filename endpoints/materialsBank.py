from endpoints import ExabyteBaseEndpoint


class ExabyteMaterialsBankEndpoint(ExabyteBaseEndpoint):
    """
    Exabyte materials-bank endpoint.

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
        self.name = 'materials-bank'
        self.user_id = user_id
        self.auth_token = auth_token
        super(ExabyteMaterialsBankEndpoint, self).__init__(host, port)
        self.headers = {'X-User-Id': self.user_id, 'X-Auth-Token': self.auth_token}

    def get_materials(self, inc_characteristics=False, page_index=0, page_size=20):
        """
        Returns a list of materials from materials-bank.

        Args:
            inc_characteristics (bool): whether to include material's characteristics.
            page_index (int): page index to return. Defaults to 0.
            page_size (int): page size. Defaults to 20.

        Returns:
            list[dict]
        """
        params = {'inc_characteristics': inc_characteristics, 'pageIndex': page_index, 'pageSize': page_size}
        return self.request('GET', self.name, params=params, headers=self.headers)

    def get_material(self, mid, inc_characteristics=False):
        """
        Returns a material with a given ID from materials-bank.

        Args:
            mid (str): material ID.
            inc_characteristics (bool): whether to include material's characteristics.

        Returns:
             dict
        """
        params = {'inc_characteristics': inc_characteristics}
        return self.request('GET', '/'.join((self.name, mid)), params=params, headers=self.headers)

    def get_materials_by_formula(self, formula, inc_characteristics=False, page_index=0, page_size=20):
        """
        Returns a list of materials with a given formula from materials-bank.

        Args:
            formula (str): material's formula.
            inc_characteristics (bool): whether to include material's characteristics.
            page_index (int): page index to return. Defaults to 0.
            page_size (int): page size. Defaults to 20.

        Returns:
            list[dict]
        """
        data = {'query': {'formula': formula}}
        params = {'inc_characteristics': inc_characteristics, 'pageIndex': page_index, 'pageSize': page_size}
        return self.request('POST', self.name, data=data, params=params, headers=self.headers)

    def delete_material(self, mid):
        """
        Deletes a given material from materials-bank.

        Args:
            mid (str): material ID.
        """
        return self.request('DELETE', '/'.join((self.name, mid)), headers=self.headers)

    def update_material(self, *args, **kwargs):
        pass

    def create_material(self, material):
        """
        Creates a new material inside materials-bank.

        Args:
            material (dict): material object.

        Returns:`
             dict
        """
        return self.request('POST', self.name, data=material, headers=self.headers)
