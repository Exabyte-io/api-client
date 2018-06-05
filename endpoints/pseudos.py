import json

from endpoints import ExabyteBaseEndpoint


class ExabytePseudosEndpoint(ExabyteBaseEndpoint):
    """
    Exabyte pseudos endpoint.

    Args:
        host (str): Exabyte API hostname.
        port (int): Exabyte API port number.
        account_id (str): account ID.
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

    def __init__(self, host, port, account_id, auth_token, version='v1', secure=True, **kwargs):
        self.name = 'pseudos'
        super(ExabytePseudosEndpoint, self).__init__(host, port, version=version, secure=secure, **kwargs)
        self.headers = {'X-Account-Id': account_id, 'X-Auth-Token': auth_token}

    def get_pseudos(self, params=None):
        """
        Returns a list of pseudos.

        Args:
            params (dict): a dictionary of parameters passed to pseudos endpoint.
                pageSize (int): page size. Defaults to 20.
                pageIndex (int): page index to return. Defaults to 0.
                query (dict): mongo query to filter the results.

        Returns:
            list[dict]
        """
        return self.request('GET', self.name, params=params, headers=self.headers)

    def get_pseudo(self, pid):
        """
        Returns a pseudo with a given ID.

        Args:
            pid (str): pseudo ID.

        Returns:
             dict: pseudo.
        """
        return self.request('GET', '/'.join((self.name, pid)), headers=self.headers)

    def upload_pseudo(self, pseudo_file):
        """
        Uploads a given pseudo.

        Args:
            pseudo_file (str): path to pseudo file.

        Returns:
             dict: new pseudo.
        """
        headers = dict([('Content-Type', 'application/json')])
        headers.update(self.headers)
        with open(pseudo_file) as f:
            pseudo = f.read()
        return self.request('POST', self.name, data=json.dumps(pseudo), headers=headers)
