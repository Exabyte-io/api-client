import mock

from exabyte_api_client.endpoints.logout import LogoutEndpoint
from tests.unit import EndpointBaseUnitTest


class EndpointLogoutUnitTest(EndpointBaseUnitTest):
    """
    Class for testing logout endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointLogoutUnitTest, self).__init__(*args, **kwargs)
        self.logout_endpoint = LogoutEndpoint(self.host, self.port, self.account_id, self.auth_token)

    @mock.patch('requests.sessions.Session.request')
    def test_logout(self, mock_request):
        mock_request.return_value = self.mock_response(self.get_content('logout.json'))
        self.assertEqual(self.logout_endpoint.logout(), {"message": "You are successfully logged out"})
        self.assertEqual(mock_request.call_args[1]['headers']['X-Account-Id'], self.account_id)
        self.assertEqual(mock_request.call_args[1]['headers']['X-Auth-Token'], self.auth_token)
