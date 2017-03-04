import mock

from endpoints.pseudos import ExabytePseudosEndpoint
from tests.unit import EndpointBaseUnitTest


class EndpointPseudosUnitTest(EndpointBaseUnitTest):
    """
    Class for testing pseudos endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointPseudosUnitTest, self).__init__(*args, **kwargs)
        self.user_id = 'ubxMkAyx37Rjn8qK9'
        self.auth_token = 'XihOnUA8EqytSui1icz6fYhsJ2tUsJGGTlV03upYPSF'
        self.pseudos_endpoint = ExabytePseudosEndpoint(self.host, self.port, self.user_id, self.auth_token)

    @mock.patch('requests.sessions.Session.request')
    def test_get_pseudos(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": []}')
        self.assertEqual(self.pseudos_endpoint.get_pseudos(), [])
        self.assertEqual(mock_request.call_args[1]['method'], 'get')

    @mock.patch('requests.sessions.Session.request')
    def test_get_pseudo(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": {}}')
        self.assertEqual(self.pseudos_endpoint.get_pseudo('28FMvD5knJZZx452H'), {})
        expected_url = 'https://{}:{}/api/v1/pseudos/28FMvD5knJZZx452H'.format(self.host, self.port)
        self.assertEqual(mock_request.call_args[1]['url'], expected_url)

    @mock.patch('requests.sessions.Session.request')
    def test_upload_pseudo(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": {}}')
        self.pseudos_endpoint.upload_pseudo(self.get_file_path('pseudo'))
        self.assertEqual(mock_request.call_args[1]['headers']['Content-Type'], 'application/json')
