import json

from endpoints import ExabyteBaseEndpoint


class ExabyteJobsEndpoint(ExabyteBaseEndpoint):
    """
    Exabyte jobs endpoint.

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
        self.name = 'jobs'
        self.user_id = user_id
        self.auth_token = auth_token
        super(ExabyteJobsEndpoint, self).__init__(host, port, version=version, secure=secure, **kwargs)
        self.headers = {'X-User-Id': self.user_id, 'X-Auth-Token': self.auth_token}

    def get_jobs(self, params=None):
        """
        Returns a list of jobs.

        Args:
            params (dict): a dictionary of parameters passed to jobs endpoint.
                pageSize (int): page size. Defaults to 20.
                pageIndex (int): page index to return. Defaults to 0.
                query (dict): mongo query to filter the results.

        Returns:
            list[dict]
        """
        return self.request('GET', self.name, params=params, headers=self.headers)

    def get_job(self, jid):
        """
        Returns a job with a given ID.

        Args:
            jid (str): job ID.

        Returns:
             dict: job.
        """
        return self.request('GET', '/'.join((self.name, jid)), headers=self.headers)

    def delete_job(self, jid):
        """
        Deletes a given job.

        Args:
            jid (str): job ID.
        """
        return self.request('DELETE', '/'.join((self.name, jid)), headers=self.headers)

    def update_job(self, jid, kwargs):
        """
        Updates a job with given key-values in kwargs.

        Args:
            jid (str): job ID.
            kwargs (dict): a dictionary of key-values to update.

        Returns:
             dict: updated job.
        """
        headers = dict([('Content-Type', 'application/json')])
        headers.update(self.headers)
        return self.request('PATCH', '/'.join((self.name, jid)), data=json.dumps(kwargs), headers=headers)

    def create_job(self, job):
        """
        Creates a new job.

        Args:
            job (dict): job object.

        Returns:
             dict: new job.
        """
        headers = dict([('Content-Type', 'application/json')])
        headers.update(self.headers)
        return self.request('POST', self.name, data=json.dumps(job), headers=headers)

    def submit_job(self, jid):
        """
        Submits a given job.

        Args:
            jid (str): job ID.
        """
        self.request('POST', '/'.join((self.name, jid)), headers=self.headers, params={'submit': True})
