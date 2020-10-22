import mock
from exabyte_api_client.endpoints.refined_properties import RefinedPropertiesEndpoints
from tests.unit.entity import EntityEndpointsUnitTest


class EndpointCharacteristicUnitTest(EntityEndpointsUnitTest):
    """
    Class for testing characteristic endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointCharacteristicUnitTest, self).__init__(*args, **kwargs)
        self.endpoint_name = "refined-properties"
        self.endpoints = RefinedPropertiesEndpoints(self.host, self.port, self.account_id, self.auth_token)

    @mock.patch('requests.sessions.Session.request')
    def test_list(self, mock_request):
        self.list(mock_request)

    @mock.patch('requests.sessions.Session.request')
    def test_get(self, mock_request):
        self.get(mock_request)
