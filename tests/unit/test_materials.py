import mock

from exabyte_api_client.endpoints.materials import MaterialEndpoints
from tests.unit.entity import EntityEndpointsUnitTest


class EndpointMaterialsUnitTest(EntityEndpointsUnitTest):
    """
    Class for testing materials endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointMaterialsUnitTest, self).__init__(*args, **kwargs)
        self.endpoint_name = "materials"
        self.endpoints = MaterialEndpoints(self.host, self.port, self.account_id, self.auth_token)

    @mock.patch('requests.sessions.Session.request')
    def test_list(self, mock_request):
        self.list(mock_request)

    @mock.patch('requests.sessions.Session.request')
    def test_get(self, mock_request):
        self.get(mock_request)

    @mock.patch('requests.sessions.Session.request')
    def test_create(self, mock_request):
        self.create(mock_request)

    @mock.patch('requests.sessions.Session.request')
    def test_delete(self, mock_request):
        self.create(mock_request)
