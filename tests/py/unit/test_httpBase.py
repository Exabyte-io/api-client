import json
from unittest import mock

from mat3ra.api_client.utils.http import Connection
from requests.exceptions import HTTPError
from tests.py.unit import EndpointBaseUnitTest

API_VERSION_1 = "2018-10-1"
API_VERSION_2 = "2018-10-2"
HTTP_STATUS_UNAUTHORIZED = 401
HTTP_STATUS_UNKNOWN = 418
EMPTY_CONTENT = ""
SERVER_MESSAGE = "Custom server error message"
SERVER_ERROR_RESPONSE = json.dumps({"message": SERVER_MESSAGE})


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
        mock_request.return_value = self.mock_response(EMPTY_CONTENT, HTTP_STATUS_UNAUTHORIZED)
        with self.assertRaises(HTTPError):
            conn = Connection(self.host, self.port, version=API_VERSION_1, secure=True)
            conn.request("POST", "login")

    @mock.patch("requests.sessions.Session.request")
    def test_http_error_message_with_server_message(self, mock_request):
        mock_request.return_value = self.mock_response(SERVER_ERROR_RESPONSE, HTTP_STATUS_UNAUTHORIZED)
        with self.assertRaises(HTTPError) as ctx:
            conn = Connection(self.host, self.port, version=API_VERSION_1, secure=True)
            conn.request("POST", "login")
        self.assertIn("Error 401", str(ctx.exception))
        self.assertIn(SERVER_MESSAGE, str(ctx.exception))

    @mock.patch("requests.sessions.Session.request")
    def test_http_error_message_without_server_message(self, mock_request):
        mock_request.return_value = self.mock_response(EMPTY_CONTENT, HTTP_STATUS_UNKNOWN)
        with self.assertRaises(HTTPError) as ctx:
            conn = Connection(self.host, self.port, version=API_VERSION_1, secure=True)
            conn.request("GET", "materials")
        self.assertIn("Error 418", str(ctx.exception))
        self.assertIn("HTTP Error", str(ctx.exception))

