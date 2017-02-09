from httpBase import ExabyteConnection


class ExabyteBaseEndpoint(object):
    """
    Base class for Exabyte endpoints.

    Args:
        host (str): Exabyte API hostname.
        port (int): Exabyte API port number.

    Attributes:
        conn (httplib.ExabyteConnection): ExabyteConnection instance.
    """

    def __init__(self, host, port):
        self.name = None
        self.headers = None
        self.conn = ExabyteConnection(host, port)

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
            # check exabyte-related errors
            return self.conn.json()

    def query(self, mongo_query):
        """
        Sends a mongo-query to the endpoint.

        Args:
            mongo_query (dict): mongo-like query.

        Returns:
            json: response
        """
        return self.request('POST', self.name, data={'query': mongo_query}, headers=self.headers)
