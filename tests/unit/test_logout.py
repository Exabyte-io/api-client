import mock

from endpoints.logout import ExabyteLogoutEndpoint
from tests.unit import EndpointBaseUnitTest


class EndpointLogoutUnitTest(EndpointBaseUnitTest):
    """
    Class for testing logout endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointLogoutUnitTest, self).__init__(*args, **kwargs)
        self.user_id = 'ubxMkAyx37Rjn8qK9'
        self.auth_token = 'XihOnUA8EqytSui1icz6fYhsJ2tUsJGGTlV03upYPSF'
        self.logout_endpoint = ExabyteLogoutEndpoint(self.host, self.port, self.user_id, self.auth_token)

    @mock.patch('requests.sessions.Session.request')
    def test_logout(self, mock_request):
        mock_request.return_value = self.mock_response(self.get_content('logout.json'))
        self.assertEqual(self.logout_endpoint.logout(), {"message": "You've been logged out!"})
        self.assertEqual(mock_request.call_args[1]['headers']['X-User-Id'], self.user_id)
        self.assertEqual(mock_request.call_args[1]['headers']['X-Auth-Token'], self.auth_token)
