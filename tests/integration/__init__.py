import os

from tests import EndpointBaseTest


class BaseIntegrationTest(EndpointBaseTest):
    """
    Base class for endpoints integration tests.
    """

    def __init__(self, *args, **kwargs):
        super(BaseIntegrationTest, self).__init__(*args, **kwargs)
        self.endpoint_kwargs = {
            'host': os.environ['HOST'],
            'port': os.environ['PORT'],
            'account_id': os.environ['ACCOUNT_ID'],
            'auth_token': os.environ['AUTH_TOKEN'],
            'secure': os.environ.get('SECURE', 'False').lower() == 'true',
            'version': os.environ.get('VERSION', '2018-10-1')
        }
