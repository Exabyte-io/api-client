from unittest import mock

from mat3ra.api_client.utils.http import Connection
from requests.exceptions import HTTPError
from tests.py.unit import EndpointBaseUnitTest

API_VERSION_1 = "2018-10-1"
API_VERSION_2 = "2018-10-2"
HTTP_STATUS_UNAUTHORIZED = 401
HTTP_REASON_UNAUTHORIZED = "Unauthorized"
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
