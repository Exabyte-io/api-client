from httpBase import ExabyteConnection


class ExabyteBaseEndpoint(object):
    """
    Base class for Exabyte endpoints.

    Args:
        host (str): Exabyte API hostname.
        port (int): Exabyte API port number.
        version (str): Exabyte API version. Defaults to v1.
        secure (bool): whether to use secure http protocol (https vs http). Defaults to True.

    Attributes:
        conn (httplib.ExabyteConnection): ExabyteConnection instance.
    """

    def __init__(self, host, port, version='v1', secure=True, **kwargs):
        self.conn = ExabyteConnection(host, port, version=version, secure=secure, **kwargs)

    def request(self, method, endpoint_path, params=None, data=None, headers=None):
        """
        Sends an HTTP request with given params, headers and data to the given endpoint.

        Args:
            method (str): HTTP method to use.
            endpoint_path (str): endpoint path.
            headers (dict): headers to send.
            data (dict): the body to attach to the request.
            params (dict): URL parameters to append to the URL.

        Returns:
            json: response
        """
        with self.conn:
            self.conn.request(method, endpoint_path, params, data, headers)
            return self.conn.json()