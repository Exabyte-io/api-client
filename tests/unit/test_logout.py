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
        self.logoutEndpoint = ExabyteLogoutEndpoint(self.host, self.port, self.user_id, self.auth_token)

    @mock.patch('endpoints.logout.ExabyteLogoutEndpoint.request')
    def test_logout(self, mock_request):
        mock_request.return_value = self.get_content_in_json('logout.json')
        expected_result = {
            "status": "success",
            "data": {
                "message": "You've been logged out!"
            }
        }
        self.assertEqual(self.logoutEndpoint.logout(), expected_result)
