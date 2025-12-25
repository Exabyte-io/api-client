from unittest import mock

from mat3ra.api_client.endpoints.logout import LogoutEndpoint
from tests.py.unit import EndpointBaseUnitTest

LOGOUT_RESPONSE_FILE = "logout.json"

EXPECTED_LOGOUT_RESULT = {
    "message": "You are successfully logged out"
}


class EndpointLogoutUnitTest(EndpointBaseUnitTest):
    """
    Class for testing logout endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointLogoutUnitTest, self).__init__(*args, **kwargs)
        self.logout_endpoint = LogoutEndpoint(self.host, self.port, self.account_id, self.auth_token)

    @mock.patch("requests.sessions.Session.request")
    def test_logout(self, mock_request):
        mock_request.return_value = self.mock_response(self.get_content(LOGOUT_RESPONSE_FILE))
        self.assertEqual(self.logout_endpoint.logout(), EXPECTED_LOGOUT_RESULT)
        self.assertEqual(mock_request.call_args[1]["headers"]["X-Account-Id"], self.account_id)
        self.assertEqual(mock_request.call_args[1]["headers"]["X-Auth-Token"], self.auth_token)
