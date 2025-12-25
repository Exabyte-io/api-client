from .entity import EntityEndpoint
from .enums import DEFAULT_API_VERSION, SECURE


class BankEntityEndpoints(EntityEndpoint):
    """
    Bank Entity endpoints.

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
    """

    def __init__(self, host, port, account_id, auth_token, version=DEFAULT_API_VERSION, secure=SECURE, **kwargs):
        super(BankEntityEndpoints, self).__init__(host, port, account_id, auth_token, version, secure, **kwargs)

    def delete(self, id_):
        raise NotImplementedError

    def update(self, id_, modifier):
        raise NotImplementedError

    def create(self, config):
        raise NotImplementedError

    def copy(self, id_, account_id=None):
        """
        Copies a bank entity with given ID into the account.

        Args:
            id_ (str): bank entity ID.
            account_id (str): ID of account to copy the bank entity into.

        Returns:
             dict: new entity.
        """
        params = {"accountId": account_id}
        return self.request("POST", "/".join((self.name, id_, "copy")), params=params, headers=self.headers)
