import mock

from requests.exceptions import HTTPError

from http_base import ExabyteConnection
from tests.unit import EndpointBaseUnitTest


class HTTPBaseUnitTest(EndpointBaseUnitTest):
    """
    Class for testing functionality implemented inside HTTPBase module.
    """

    def __init__(self, *args, **kwargs):
        super(HTTPBaseUnitTest, self).__init__(*args, **kwargs)

    def test_preamble_secure(self):
        conn = ExabyteConnection(self.host, self.port, version='v1', secure=True)
        self.assertEqual(conn.preamble, 'https://{}:{}/api/v1/'.format(self.host, self.port))

    def test_preamble_unsecure(self):
        conn = ExabyteConnection(self.host, self.port, version='v1', secure=False)
        self.assertEqual(conn.preamble, 'http://{}:{}/api/v1/'.format(self.host, self.port))

    def test_preamble_version(self):
        conn = ExabyteConnection(self.host, self.port, version='v2', secure=True)
        self.assertEqual(conn.preamble, 'https://{}:{}/api/v2/'.format(self.host, self.port))

    @mock.patch('requests.sessions.Session.request')
    def test_raise_http_error(self, mock_request):
        mock_request.return_value = self.mock_response('', 401, reason='Unauthorized')
        with self.assertRaises(HTTPError):
            conn = ExabyteConnection(self.host, self.port, version='v1', secure=True)
            conn.request('POST', 'login', data={'username': '', 'password': ''})
