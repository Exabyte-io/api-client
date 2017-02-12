import mock

from endpoints.materials import ExabyteMaterialsEndpoint
from tests.unit import EndpointBaseUnitTest


class EndpointMaterialsUnitTest(EndpointBaseUnitTest):
    """
    Class for testing materials endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointMaterialsUnitTest, self).__init__(*args, **kwargs)
        self.user_id = 'ubxMkAyx37Rjn8qK9'
        self.auth_token = 'XihOnUA8EqytSui1icz6fYhsJ2tUsJGGTlV03upYPSF'
        self.materials_endpoint = ExabyteMaterialsEndpoint(self.host, self.port, self.user_id, self.auth_token)

    @mock.patch('requests.sessions.Session.request')
    def test_get_materials(self, mock_request):
        mock_request.return_value = self.mock_response('[]')
        self.assertEqual(self.materials_endpoint.get_materials(), [])
        self.assertEqual(mock_request.call_args[1]['method'], 'get')

    @mock.patch('requests.sessions.Session.request')
    def test_get_material(self, mock_request):
        mock_request.return_value = self.mock_response('{}')
        self.assertEqual(self.materials_endpoint.get_material('28FMvD5knJZZx452H'), {})
        expected_url = 'https://{}:{}/api/v1/materials/28FMvD5knJZZx452H'.format(self.host, self.port)
        self.assertEqual(mock_request.call_args[1]['url'], expected_url)

    @mock.patch('requests.sessions.Session.request')
    def test_get_material_by_formula(self, mock_request):
        mock_request.return_value = self.mock_response('[]')
        self.assertEqual(self.materials_endpoint.get_materials_by_formula('Si'), [])
        self.assertEqual(mock_request.call_args[1]['params'], {'query': '{"formula": "Si"}'})

    @mock.patch('requests.sessions.Session.request')
    def test_create_material(self, mock_request):
        mock_request.return_value = self.mock_response(self.get_content('new-material.json'))
        self.materials_endpoint.create_material(self.get_content_in_json('new-material.json'))
        self.assertEqual(mock_request.call_args[1]['headers']['Content-Type'], 'application/json')

    @mock.patch('requests.sessions.Session.request')
    def test_delete_material(self, mock_request):
        mock_request.return_value = self.mock_response('{}')
        self.assertEqual(self.materials_endpoint.delete_material('28FMvD5knJZZx452H'), {})
        self.assertEqual(mock_request.call_args[1]['method'], 'delete')
