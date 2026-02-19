from typing import List

from mat3ra.ide import Cluster

from . import BaseEndpoint
from .enums import DEFAULT_API_VERSION, SECURE


class ClustersEndpoint(BaseEndpoint):
    """
    Clusters endpoints for infrastructure access.

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
        headers (dict): default HTTP headers.
    """

    def __init__(self, host, port, account_id, auth_token, version=DEFAULT_API_VERSION, secure=SECURE, **kwargs):
        super(ClustersEndpoint, self).__init__(host, port, version, secure, **kwargs)
        self.headers = self.get_headers(account_id, auth_token)

    def list(self) -> List[Cluster]:
        """
        Returns a list of available clusters.

        Returns:
            list[Cluster]: List of Cluster objects with fqdn set to the cluster hostname.
        """
        response = self.request("GET", "infrastructure/clusters", headers=self.headers)
        return [Cluster(fqdn=cluster_data["hostname"]) for cluster_data in response]
