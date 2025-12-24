from requests import Response

from tests.conftest import EndpointBaseTest

DEFAULT_TEST_PORT = 4000
DEFAULT_TEST_VERSION = "2018-10-01"
DEFAULT_TEST_HOST = "platform.mat3ra.com"
DEFAULT_TEST_ACCOUNT_ID = "ubxMkAyx37Rjn8qK9"
DEFAULT_TEST_AUTH_TOKEN = "XihOnUA8EqytSui1icz6fYhsJ2tUsJGGTlV03upYPSF"
HTTP_STATUS_OK = 200
HTTP_REASON_OK = "OK"


class EndpointBaseUnitTest(EndpointBaseTest):
    """
    Base class for endpoints unit tests.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointBaseUnitTest, self).__init__(*args, **kwargs)
        self.port = DEFAULT_TEST_PORT
        self.version = DEFAULT_TEST_VERSION
        self.host = DEFAULT_TEST_HOST
        self.account_id = DEFAULT_TEST_ACCOUNT_ID
        self.auth_token = DEFAULT_TEST_AUTH_TOKEN

    def mock_response(self, content, status_code=HTTP_STATUS_OK, reason=HTTP_REASON_OK):
        response = Response()
        response._content = content.encode()
        response.status_code = status_code
        response.reason = reason
        return response
