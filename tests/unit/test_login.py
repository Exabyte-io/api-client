import mock

from endpoints.login import ExabyteLoginEndpoint
from tests.unit import EndpointBaseUnitTest


class EndpointLoginUnitTest(EndpointBaseUnitTest):
    """
    Class for testing login endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointLoginUnitTest, self).__init__(*args, **kwargs)
        self.username = 'test'
        self.password = 'test'
        self.loginEndpoint = ExabyteLoginEndpoint(self.host, self.port, self.username, self.password)

    @mock.patch('endpoints.login.ExabyteLoginEndpoint.request')
    def test_login(self, mock_request):
        mock_request.return_value = self.get_content_in_json('login.json')
        expected_result = {
            'user_id': 'ubxMkAyx37Rjn8qK9',
            'auth_token': 'XihOnUA8EqytSui1icz6fYhsJ2tUsJGGTlV03upYPSF'
        }
        self.assertEqual(self.loginEndpoint.login(), expected_result)
