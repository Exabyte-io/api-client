from .entity import EntityEndpoint
from .enums import DEFAULT_API_VERSION, SECURE


class ChargeEndpoints(EntityEndpoint):
    """
    Charge endpoints.

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
        user_id (str): user ID.
        auth_token (str): authentication token.
        headers (dict): default HTTP headers.
    """

    def __init__(self, host, port, account_id, auth_token, version=DEFAULT_API_VERSION, secure=SECURE, **kwargs):
        super(ChargeEndpoints, self).__init__(host, port, account_id, auth_token, version, secure, **kwargs)
        self.name = "charges"

    def delete(self, id_):
        raise NotImplementedError

    def update(self, id_, modifier):
        raise NotImplementedError

    def create(self, config):
        raise NotImplementedError

    def get_by_job(self, job):
        return next(iter(self.list(query={"jid": job["compute"]["cluster"]["jid"]})), None)
