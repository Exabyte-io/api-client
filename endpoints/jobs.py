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

    def get_config(self, material_id, workflow_id, project_id, owner_id, compute, name):
        return {
            "_project": {
                "_id": project_id
            },
            "_material": {
                "_id": material_id
            },
            "workflow": {
                "_id": workflow_id
            },
            "owner": {
                "_id": owner_id
            },
            "compute": compute,
            "name": name
        }

    def get_compute(self, cluster, ppn=1, nodes=1, queue="D", time_limit="01:00:00", notify="abe"):
        return {
            "ppn": ppn,
            "nodes": nodes,
            "queue": queue,
            "timeLimit": time_limit,
            "notify": notify,
            "cluster": {
                "fqdn": cluster
            },
            "arguments": {}
        }

    def create_by_ids(self, materials, workflow_id, project_id, owner_id, compute, prefix):
        """
        Creates jobs from the given materials

        Args:
            materials (list[dict]): list of materials.
            workflow_id (str): workflow ID.
            project_id (str): project ID.
            owner_id (str): owner ID.
            compute (dict): compute configuration.
            prefix (str): job prefix.

        Returns:
            list
        """
        jobs = []
        for material in materials:
            job_name = "-".join((prefix, material["formula"])),
            job_config = self.get_config(material["_id"], workflow_id, project_id, owner_id, compute, job_name)
            jobs.append(self.create(job_config))
        return jobs
