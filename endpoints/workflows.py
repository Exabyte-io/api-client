import json

from endpoints import ExabyteBaseEndpoint


class ExabyteWorkflowsEndpoint(ExabyteBaseEndpoint):
    """
    Exabyte workflows endpoint.

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
        self.name = 'workflows'
        super(ExabyteWorkflowsEndpoint, self).__init__(host, port, version=version, secure=secure, **kwargs)
        self.headers = {'X-Account-Id': account_id, 'X-Auth-Token': auth_token}

    def get_workflows(self, params=None):
        """
        Returns a list of workflows.

        Args:
            params (dict): a dictionary of parameters passed to workflows endpoint.
                pageSize (int): page size. Defaults to 20.
                pageIndex (int): page index to return. Defaults to 0.
                query (dict): mongo query to filter the results.

        Returns:
            list[dict]
        """
        return self.request('GET', self.name, params=params, headers=self.headers)

    def get_workflow(self, wid):
        """
        Returns a workflow with a given ID.

        Args:
            wid (str): workflow ID.

        Returns:
             dict: workflow.
        """
        return self.request('GET', '/'.join((self.name, wid)), headers=self.headers)

    def delete_workflow(self, wid):
        """
        Deletes a given workflow.

        Args:
            wid (str): workflow ID.
        """
        return self.request('DELETE', '/'.join((self.name, wid)), headers=self.headers)

    def update_workflow(self, wid, kwargs):
        """
        Updates a workflow with given key-values in kwargs.

        Args:
            wid (str): workflow ID.
            kwargs (dict): a dictionary of key-values to update.

        Returns:
             dict: updated workflow.
        """
        headers = dict([('Content-Type', 'application/json')])
        headers.update(self.headers)
        return self.request('PATCH', '/'.join((self.name, wid)), data=json.dumps(kwargs), headers=headers)

    def create_workflow(self, workflow):
        """
        Creates a new Workflow.

        Args:
            workflow (dict): workflow object.

        Returns:
             dict: new workflow.
        """
        headers = dict([('Content-Type', 'application/json')])
        headers.update(self.headers)
        return self.request('POST', self.name, data=json.dumps(workflow), headers=headers)
