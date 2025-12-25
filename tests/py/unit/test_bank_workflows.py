from unittest import mock

from mat3ra.api_client.endpoints.bank_workflows import BankWorkflowEndpoints
from tests.py.unit.entity import EntityEndpointsUnitTest

ENDPOINT_NAME = "bank-workflows"


class EndpointWorkflowsBankUnitTest(EntityEndpointsUnitTest):
    """
    Class for testing bank workflows endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointWorkflowsBankUnitTest, self).__init__(*args, **kwargs)
        self.endpoint_name = ENDPOINT_NAME
        self.endpoints = BankWorkflowEndpoints(self.host, self.port, self.account_id, self.auth_token)

    @mock.patch("requests.sessions.Session.request")
    def test_list(self, mock_request):
        self.list(mock_request)

    @mock.patch("requests.sessions.Session.request")
    def test_get(self, mock_request):
        self.get(mock_request)
