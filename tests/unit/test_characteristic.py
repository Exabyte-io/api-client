import mock

from endpoints.characteristic import ExabyteCharacteristicEndpoint
from tests.unit import EndpointBaseUnitTest


class EndpointCharacteristicUnitTest(EndpointBaseUnitTest):
    """
    Class for testing characteristic endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointCharacteristicUnitTest, self).__init__(*args, **kwargs)
        self.user_id = 'ubxMkAyx37Rjn8qK9'
        self.auth_token = 'XihOnUA8EqytSui1icz6fYhsJ2tUsJGGTlV03upYPSF'
        self.char_endpoint = ExabyteCharacteristicEndpoint(self.host, self.port, self.user_id, self.auth_token)

    @mock.patch('requests.sessions.Session.request')
    def test_get_characteristics(self, mock_request):
        mock_request.return_value = self.mock_response('[]')
        self.assertEqual(self.char_endpoint.get_characteristics(), [])
        self.assertEqual(mock_request.call_args[1]['method'], 'get')

    @mock.patch('requests.sessions.Session.request')
    def test_get_characteristic(self, mock_request):
        mock_request.return_value = self.mock_response('{}')
        self.assertEqual(self.char_endpoint.get_characteristic('28FMvD5knJZZx452H'), {})
        expected_url = 'https://{}:{}/api/v1/characteristic/28FMvD5knJZZx452H'.format(self.host, self.port)
        self.assertEqual(mock_request.call_args[1]['url'], expected_url)

    @mock.patch('requests.sessions.Session.request')
    def test_create_characteristic(self, mock_request):
        mock_request.return_value = self.mock_response(self.get_content('new-characteristic.json'))
        self.char_endpoint.create_characteristic(self.get_content_in_json('new-characteristic.json'))
        self.assertEqual(mock_request.call_args[1]['headers']['Content-Type'], 'application/json')

    @mock.patch('requests.sessions.Session.request')
    def test_delete_characteristic(self, mock_request):
        mock_request.return_value = self.mock_response('{}')
        self.assertEqual(self.char_endpoint.delete_characteristic('28FMvD5knJZZx452H'), {})
        self.assertEqual(mock_request.call_args[1]['method'], 'delete')
