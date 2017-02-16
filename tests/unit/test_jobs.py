import mock

from endpoints.jobs import ExabyteJobsEndpoint
from tests.unit import EndpointBaseUnitTest


class EndpointJobsUnitTest(EndpointBaseUnitTest):
    """
    Class for testing jobs endpoint.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointJobsUnitTest, self).__init__(*args, **kwargs)
        self.user_id = 'ubxMkAyx37Rjn8qK9'
        self.auth_token = 'XihOnUA8EqytSui1icz6fYhsJ2tUsJGGTlV03upYPSF'
        self.jobs_endpoint = ExabyteJobsEndpoint(self.host, self.port, self.user_id, self.auth_token)

    @mock.patch('requests.sessions.Session.request')
    def test_get_materials(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": []}')
        self.assertEqual(self.jobs_endpoint.get_jobs(), [])
        self.assertEqual(mock_request.call_args[1]['method'], 'get')

    @mock.patch('requests.sessions.Session.request')
    def test_get_material(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": {}}')
        self.assertEqual(self.jobs_endpoint.get_job('28FMvD5knJZZx452H'), {})
        expected_url = 'https://{}:{}/api/v1/jobs/28FMvD5knJZZx452H'.format(self.host, self.port)
        self.assertEqual(mock_request.call_args[1]['url'], expected_url)

    @mock.patch('requests.sessions.Session.request')
    def test_create_material(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": {}}')
        self.jobs_endpoint.create_job(self.get_content_in_json('new-job.json'))
        self.assertEqual(mock_request.call_args[1]['headers']['Content-Type'], 'application/json')

    @mock.patch('requests.sessions.Session.request')
    def test_delete_material(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": {}}')
        self.assertEqual(self.jobs_endpoint.delete_job('28FMvD5knJZZx452H'), {})
        self.assertEqual(mock_request.call_args[1]['method'], 'delete')
