from requests import Response

from tests import EndpointBaseTest


class EndpointBaseUnitTest(EndpointBaseTest):
    """
    Base class for endpoints unit tests.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointBaseUnitTest, self).__init__(*args, **kwargs)
        self.host = 'platform.exabyte.io'
        self.port = 4000

    def mock_response(self, content, status_code=200, reason='OK'):
        response = Response()
        response._content = content
        response.status_code = status_code
        response.reason = reason
        return response
