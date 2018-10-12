from endpoints.entity import EntityEndpoint
from endpoints.enums import DEFAULT_API_VERSION, SECURE
from endpoints.mixins.set import EntitySetEndpointsMixin


class JobEndpoints(EntitySetEndpointsMixin, EntityEndpoint):
    """
    Job endpoints.

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
    """

    def __init__(self, host, port, account_id, auth_token, version=DEFAULT_API_VERSION, secure=SECURE, **kwargs):
        super(JobEndpoints, self).__init__(host, port, account_id, auth_token, version, secure, **kwargs)
        self.name = 'jobs'

    def submit(self, id_):
        """
        Submits a given job.

        Args:
            id_ (str): job ID.
        """
        self.request('POST', '/'.join((self.name, id_, "submit")), headers=self.headers)

    def purge(self, id_):
        """
        Purges a given job.

        Args:
            id_ (str): job ID.
        """
        self.request('POST', '/'.join((self.name, id_, "submit")), headers=self.headers)

    def terminate(self, id_):
        """
        Terminates a given job.

        Args:
            id_ (str): job ID.
        """
        self.request('POST', '/'.join((self.name, id_, "submit")), headers=self.headers)
