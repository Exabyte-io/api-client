import mock
from exabyte_api_client.endpoints.bank_materials import BankMaterialEndpoints
from tests.unit.entity import EntityEndpointsUnitTest


class EndpointMaterialsBankUnitTest(EntityEndpointsUnitTest):
    """
    Class for testing bank materials endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointMaterialsBankUnitTest, self).__init__(*args, **kwargs)
        self.endpoint_name = "bank-materials"
        self.endpoints = BankMaterialEndpoints(self.host, self.port, self.account_id, self.auth_token)

    @mock.patch('requests.sessions.Session.request')
    def test_list(self, mock_request):
        self.list(mock_request)

    @mock.patch('requests.sessions.Session.request')
    def test_get(self, mock_request):
        self.get(mock_request)
