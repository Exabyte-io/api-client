import os

from tests import EndpointBaseTest


class BaseIntegrationTest(EndpointBaseTest):
    """
    Base class for endpoints integration tests.
    """

    def __init__(self, *args, **kwargs):
        super(BaseIntegrationTest, self).__init__(*args, **kwargs)
        self.endpoint_kwargs = {
            'host': os.environ['TEST_HOST'],
            'port': os.environ['TEST_PORT'],
            'account_id': os.environ['TEST_ACCOUNT_ID'],
            'auth_token': os.environ['TEST_AUTH_TOKEN'],
            'secure': os.environ.get('TEST_SECURE', 'False').lower() == 'true',
            'version': os.environ.get('TEST_VERSION', '2018-10-01')
        }
