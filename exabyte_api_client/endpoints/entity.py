import json

from . import BaseEndpoint
from .enums import DEFAULT_API_VERSION, SECURE


class EntityEndpoint(BaseEndpoint):
    """
    Exabyte Entity endpoint.

    Args:
        host (str): Exabyte API hostname.
        port (int): Exabyte API port number.
        account_id (str): account ID.
        auth_token (str): authentication token.
        version (str): Exabyte API version.
        secure (bool): whether to use secure http protocol (https vs http).
        kwargs (dict): a dictionary of HTTP session options.
            timeout (int): session timeout in seconds.

    Attributes:
        name (str): endpoint name.
        headers (dict): default HTTP headers.
    """

    def __init__(self, host, port, account_id, auth_token, version=DEFAULT_API_VERSION, secure=SECURE, **kwargs):
        super(EntityEndpoint, self).__init__(host, port, version, secure, **kwargs)
        self.name = None
        self.headers = self.get_headers(account_id, auth_token)

    def list(self, query=None, projection=None):
        """
        Returns a list of entities.

        Args:
            query (dict): Mongo query. Defaults to {}.
            projection (dict): Mongo projection. Defaults to {}.

        Returns:
            list[dict]
        """
        params = {"query": json.dumps(query or {}), "projection": json.dumps(projection or {})}
        return self.request('GET', self.name, params=params, headers=self.headers)

    def get(self, id_):
        """
        Returns a entity with given ID.

        Args:
            id_ (str): entity ID.

        Returns:
             dict: entity.
        """
        return self.request('GET', '/'.join((self.name, id_)), headers=self.headers)

    def delete(self, id_):
        """
        Deletes a given entity.

        Args:
            id_ (str): entity ID.
        """
        return self.request('DELETE', '/'.join((self.name, id_)), headers=self.headers)

    def update(self, id_, modifier):
        """
        Updates a entity with given ID.

        Args:
            id_ (str): entity ID.
            modifier (dict): a dictionary of key-values to update entity with.

        Returns:
             dict: updated entity.
        """
        return self.request('PATCH', '/'.join((self.name, id_)), data=json.dumps(modifier), headers=self.headers)

    def create(self, config):
        """
        Creates a new entity.

        Args:
            config (dict): entity config.

        Returns:
             dict: new entity.
        """
        return self.request('PUT', '/'.join((self.name, "create")), data=json.dumps(config), headers=self.headers)

    def copy(self, id_):
        """
        Copies a entity with given ID.

        Args:
            id_ (str): entity ID.

        Returns:
             dict: new entity.
        """
        return self.request('POST', '/'.join((self.name, id_, "copy")), headers=self.headers)
