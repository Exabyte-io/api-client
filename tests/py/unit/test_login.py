from unittest import mock

from mat3ra.api_client.endpoints.login import LoginEndpoint
from tests.py.unit import EndpointBaseUnitTest

TEST_USERNAME = "test"
TEST_PASSWORD = "test"
LOGIN_RESPONSE_FILE = "login.json"

EXPECTED_LOGIN_RESULT = {
    "X-Account-Id": "ubxMkAyx37Rjn8qK9",
    "X-Auth-Token": "XihOnUA8EqytSui1icz6fYhsJ2tUsJGGTlV03upYPSF",
}


class EndpointLoginUnitTest(EndpointBaseUnitTest):
    """
    Class for testing login endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointLoginUnitTest, self).__init__(*args, **kwargs)
        self.username = TEST_USERNAME
        self.password = TEST_PASSWORD
        self.login_endpoint = LoginEndpoint(self.host, self.port, self.username, self.password)

    @mock.patch("requests.sessions.Session.request")
    def test_login(self, mock_request):
        mock_request.return_value = self.mock_response(self.get_content(LOGIN_RESPONSE_FILE))
        self.assertEqual(self.login_endpoint.login(), EXPECTED_LOGIN_RESULT)
        self.assertEqual(mock_request.call_args[1]["data"]["username"], self.username)
        self.assertEqual(mock_request.call_args[1]["data"]["password"], self.password)
