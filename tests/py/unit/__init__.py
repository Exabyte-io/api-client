from requests import Response

from tests.py.conftest import EndpointBaseTest


class EndpointBaseUnitTest(EndpointBaseTest):
    """
    Base class for endpoints unit tests.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointBaseUnitTest, self).__init__(*args, **kwargs)
        self.port = 4000
        self.version = "2018-10-01"
        self.host = "platform.mat3ra.com"
        self.account_id = "ubxMkAyx37Rjn8qK9"
        self.auth_token = "XihOnUA8EqytSui1icz6fYhsJ2tUsJGGTlV03upYPSF"

    def mock_response(self, content, status_code=200, reason="OK"):
        response = Response()
        response._content = content.encode()
        response.status_code = status_code
        response.reason = reason
        return response
