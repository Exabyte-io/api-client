from unittest import mock

from mat3ra.api_client.utils.http import Connection
from requests.exceptions import HTTPError
from tests.py.unit import EndpointBaseUnitTest

API_VERSION_1 = "2018-10-1"
API_VERSION_2 = "2018-10-2"
HTTP_STATUS_UNAUTHORIZED = 401
HTTP_REASON_UNAUTHORIZED = "Unauthorized"
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500
HTTP_REASON_INTERNAL_SERVER_ERROR = "Internal Server Error"
HTTP_STATUS_TOO_MANY_REQUESTS = 429
HTTP_REASON_TOO_MANY_REQUESTS = "Too Many Requests"
HTTP_STATUS_FORBIDDEN = 403
HTTP_REASON_FORBIDDEN = "Forbidden"
HTTP_STATUS_UNKNOWN = 418
HTTP_REASON_UNKNOWN = "I'm a Teapot"
EMPTY_CONTENT = ""
TEST_ENTITY_ID = "28FMvD5knJZZx452H"
EMPTY_USERNAME = ""
EMPTY_PASSWORD = ""


class HTTPBaseUnitTest(EndpointBaseUnitTest):
    """
    Class for testing functionality implemented inside HTTPBase module.
    """

    def __init__(self, *args, **kwargs):
        super(HTTPBaseUnitTest, self).__init__(*args, **kwargs)

    def test_preamble_secure(self):
        conn = Connection(self.host, self.port, version=API_VERSION_1, secure=True)
        self.assertEqual(conn.preamble, f"https://{self.host}:{self.port}/api/{API_VERSION_1}/")

    def test_preamble_unsecure(self):
        conn = Connection(self.host, self.port, version=API_VERSION_1, secure=False)
        self.assertEqual(conn.preamble, f"http://{self.host}:{self.port}/api/{API_VERSION_1}/")

    def test_preamble_version(self):
        conn = Connection(self.host, self.port, version=API_VERSION_2, secure=True)
        self.assertEqual(conn.preamble, f"https://{self.host}:{self.port}/api/{API_VERSION_2}/")

    @mock.patch("requests.sessions.Session.request")
    def test_raise_http_error(self, mock_request):
        mock_request.return_value = self.mock_response(EMPTY_CONTENT, HTTP_STATUS_UNAUTHORIZED,
                                                       reason=HTTP_REASON_UNAUTHORIZED)
        with self.assertRaises(HTTPError):
            conn = Connection(self.host, self.port, version=API_VERSION_1, secure=True)
            conn.request("POST", "login", data={"username": EMPTY_USERNAME, "password": EMPTY_PASSWORD})

    @mock.patch("requests.sessions.Session.request")
    def test_http_error_message_known_status(self, mock_request):
        mock_request.return_value = self.mock_response(EMPTY_CONTENT, HTTP_STATUS_UNAUTHORIZED,
                                                       reason=HTTP_REASON_UNAUTHORIZED)
        with self.assertRaises(HTTPError) as ctx:
            conn = Connection(self.host, self.port, version=API_VERSION_1, secure=True)
            conn.request("POST", "login", data={"username": EMPTY_USERNAME, "password": EMPTY_PASSWORD})
        self.assertIn("Error 401", str(ctx.exception))
        self.assertIn("Unauthorized", str(ctx.exception))
        self.assertIn("authentication token", str(ctx.exception))

    @mock.patch("requests.sessions.Session.request")
    def test_http_error_message_500(self, mock_request):
        mock_request.return_value = self.mock_response(EMPTY_CONTENT, HTTP_STATUS_INTERNAL_SERVER_ERROR,
                                                       reason=HTTP_REASON_INTERNAL_SERVER_ERROR)
        with self.assertRaises(HTTPError) as ctx:
            conn = Connection(self.host, self.port, version=API_VERSION_1, secure=True)
            conn.request("POST", "jobs/id/submit")
        self.assertIn("Error 500", str(ctx.exception))
        self.assertIn("Internal Server Error", str(ctx.exception))
        self.assertIn("Contact support", str(ctx.exception))

    @mock.patch("requests.sessions.Session.request")
    def test_http_error_message_429_quota(self, mock_request):
        mock_request.return_value = self.mock_response(EMPTY_CONTENT, HTTP_STATUS_TOO_MANY_REQUESTS,
                                                       reason=HTTP_REASON_TOO_MANY_REQUESTS)
        with self.assertRaises(HTTPError) as ctx:
            conn = Connection(self.host, self.port, version=API_VERSION_1, secure=True)
            conn.request("POST", "materials")
        self.assertIn("Error 429", str(ctx.exception))
        self.assertIn("quota", str(ctx.exception))

    @mock.patch("requests.sessions.Session.request")
    def test_http_error_message_403_project(self, mock_request):
        mock_request.return_value = self.mock_response(EMPTY_CONTENT, HTTP_STATUS_FORBIDDEN,
                                                       reason=HTTP_REASON_FORBIDDEN)
        with self.assertRaises(HTTPError) as ctx:
            conn = Connection(self.host, self.port, version=API_VERSION_1, secure=True)
            conn.request("GET", "workflows")
        self.assertIn("Error 403", str(ctx.exception))
        self.assertIn("project", str(ctx.exception))

    @mock.patch("requests.sessions.Session.request")
    def test_http_error_message_unknown_status(self, mock_request):
        mock_request.return_value = self.mock_response(EMPTY_CONTENT, HTTP_STATUS_UNKNOWN,
                                                       reason=HTTP_REASON_UNKNOWN)
        with self.assertRaises(HTTPError) as ctx:
            conn = Connection(self.host, self.port, version=API_VERSION_1, secure=True)
            conn.request("GET", "materials")
        self.assertIn("Error 418", str(ctx.exception))
        self.assertIn("HTTP Error", str(ctx.exception))

