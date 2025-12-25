from .entity import EntityEndpoint
from .enums import DEFAULT_API_VERSION, SECURE


class BasePropertiesEndpoints(EntityEndpoint):
    def get_property_selector(self, job_id, unit_flowchart_id, property_name):
        return {"source.info.jobId": job_id, "source.info.unitId": unit_flowchart_id, "data.name": property_name}

    def get_property(self, job_id, unit_flowchart_id, property_name):
        selector = self.get_property_selector(job_id, unit_flowchart_id, property_name)
        return self.list(query=selector)[0]

    def get_band_gap_by_type(self, job_id, unit_flowchart_id, type):
        band_gaps = self.get_property(job_id, unit_flowchart_id, "band_gaps")["data"]
        return next((v for v in band_gaps["values"] if v["type"] == type), None)["value"]

    def get_indirect_band_gap(self, job_id, unit_flowchart_id):
        return self.get_band_gap_by_type(job_id, unit_flowchart_id, "indirect")

    def get_direct_band_gap(self, job_id, unit_flowchart_id):
        return self.get_band_gap_by_type(job_id, unit_flowchart_id, "direct")


class PropertiesEndpoints(BasePropertiesEndpoints):
    """
    Properties endpoints.

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
        user_id (str): user ID.
        auth_token (str): authentication token.
        headers (dict): default HTTP headers.
    """

    def __init__(self, host, port, account_id, auth_token, version=DEFAULT_API_VERSION, secure=SECURE, **kwargs):
        super(PropertiesEndpoints, self).__init__(host, port, account_id, auth_token, version, secure, **kwargs)
        self.name = "properties"

    def delete(self, id_):
        raise NotImplementedError

    def update(self, id_, modifier):
        raise NotImplementedError
