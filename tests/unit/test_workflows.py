import mock

from endpoints.workflows import ExabyteWorkflowsEndpoint
from tests.unit import EndpointBaseUnitTest


class EndpointWorkflowsUnitTest(EndpointBaseUnitTest):
    """
    Class for testing workflows endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointWorkflowsUnitTest, self).__init__(*args, **kwargs)
        self.user_id = 'ubxMkAyx37Rjn8qK9'
        self.auth_token = 'XihOnUA8EqytSui1icz6fYhsJ2tUsJGGTlV03upYPSF'
        self.workflows_endpoint = ExabyteWorkflowsEndpoint(self.host, self.port, self.user_id, self.auth_token)

    @mock.patch('requests.sessions.Session.request')
    def test_get_workflows(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": []}')
        self.assertEqual(self.workflows_endpoint.get_workflows(), [])
        self.assertEqual(mock_request.call_args[1]['method'], 'get')

    @mock.patch('requests.sessions.Session.request')
    def test_get_workflow(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": {}}')
        self.assertEqual(self.workflows_endpoint.get_workflow('28FMvD5knJZZx452H'), {})
        expected_url = 'https://{}:{}/api/v1/workflows/28FMvD5knJZZx452H'.format(self.host, self.port)
        self.assertEqual(mock_request.call_args[1]['url'], expected_url)

    @mock.patch('requests.sessions.Session.request')
    def test_create_workflow(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": {}}')
        self.workflows_endpoint.create_workflow(self.get_content_in_json('workflow.json'))
        self.assertEqual(mock_request.call_args[1]['headers']['Content-Type'], 'application/json')

    @mock.patch('requests.sessions.Session.request')
    def test_delete_workflow(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": {}}')
        self.assertEqual(self.workflows_endpoint.delete_workflow('28FMvD5knJZZx452H'), {})
        self.assertEqual(mock_request.call_args[1]['method'], 'delete')
