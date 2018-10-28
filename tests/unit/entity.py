from tests.unit import EndpointBaseUnitTest


class EntityEndpointsUnitTest(EndpointBaseUnitTest):
    """
    Base class for testing entity endpoints.
    """

    def __init__(self, *args, **kwargs):
        super(EntityEndpointsUnitTest, self).__init__(*args, **kwargs)
        self.endpoints = None
        self.endpoint_name = None

    @property
    def base_url(self):
        return 'https://{}:{}/api/{}/{}'.format(self.host, self.port, self.version, self.endpoint_name)

    def list(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": []}')
        self.assertEqual(self.endpoints.list(), [])
        self.assertEqual(mock_request.call_args[1]['method'], 'get')

    def get(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": {}}')
        self.assertEqual(self.endpoints.get('28FMvD5knJZZx452H'), {})
        expected_url = '{}/28FMvD5knJZZx452H'.format(self.base_url, self.port)
        self.assertEqual(mock_request.call_args[1]['url'], expected_url)

    def create(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": {}}')
        self.endpoints.create({})
        self.assertEqual(mock_request.call_args[1]['headers']['Content-Type'], 'application/json')

    def delete(self, mock_request):
        mock_request.return_value = self.mock_response('{"status": "success", "data": {}}')
        self.assertEqual(self.endpoints.delete('28FMvD5knJZZx452H'), {})
        self.assertEqual(mock_request.call_args[1]['method'], 'delete')
