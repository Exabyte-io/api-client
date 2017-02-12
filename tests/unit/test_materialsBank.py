import mock

from endpoints.materialsBank import ExabyteMaterialsBankEndpoint
from tests.unit import EndpointBaseUnitTest


class EndpointMaterialsBankUnitTest(EndpointBaseUnitTest):
    """
    Class for testing materials-bank endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointMaterialsBankUnitTest, self).__init__(*args, **kwargs)
        self.user_id = 'ubxMkAyx37Rjn8qK9'
        self.auth_token = 'XihOnUA8EqytSui1icz6fYhsJ2tUsJGGTlV03upYPSF'
        self.materials_bank_endpoint = ExabyteMaterialsBankEndpoint(self.host, self.port, self.user_id, self.auth_token)

    @mock.patch('requests.sessions.Session.request')
    def test_get_materials(self, mock_request):
        mock_request.return_value = self.mock_response('[]')
        self.assertEqual(self.materials_bank_endpoint.get_materials(), [])
        self.assertEqual(mock_request.call_args[1]['method'], 'get')

    @mock.patch('requests.sessions.Session.request')
    def test_get_material(self, mock_request):
        mock_request.return_value = self.mock_response('{}')
        self.assertEqual(self.materials_bank_endpoint.get_material('28FMvD5knJZZx452H'), {})
        expected_url = 'https://{}:{}/api/v1/materials-bank/28FMvD5knJZZx452H'.format(self.host, self.port)
        self.assertEqual(mock_request.call_args[1]['url'], expected_url)

    @mock.patch('requests.sessions.Session.request')
    def test_get_material_by_formula(self, mock_request):
        mock_request.return_value = self.mock_response('[]')
        self.assertEqual(self.materials_bank_endpoint.get_materials_by_formula('Si'), [])
        self.assertEqual(mock_request.call_args[1]['params'], {'query': '{"formula": "Si"}'})
