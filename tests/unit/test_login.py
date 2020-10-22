import mock

from exabyte_api_client.endpoints.login import LoginEndpoint
from tests.unit import EndpointBaseUnitTest


class EndpointLoginUnitTest(EndpointBaseUnitTest):
    """
    Class for testing login endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointLoginUnitTest, self).__init__(*args, **kwargs)
        self.username = 'test'
        self.password = 'test'
        self.login_endpoint = LoginEndpoint(self.host, self.port, self.username, self.password)

    @mock.patch('requests.sessions.Session.request')
    def test_login(self, mock_request):
        mock_request.return_value = self.mock_response(self.get_content('login.json'))
        expected_result = {
            'X-Account-Id': 'ubxMkAyx37Rjn8qK9',
            'X-Auth-Token': 'XihOnUA8EqytSui1icz6fYhsJ2tUsJGGTlV03upYPSF'
        }
        self.assertEqual(self.login_endpoint.login(), expected_result)
        self.assertEqual(mock_request.call_args[1]['data']['username'], self.username)
        self.assertEqual(mock_request.call_args[1]['data']['password'], self.password)
