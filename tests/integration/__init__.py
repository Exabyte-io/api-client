import os

from tests import EndpointBaseTest


class EndpointBaseIntegrationTest(EndpointBaseTest):
    """
    Base class for endpoints integration tests.
    """

    def __init__(self, *args, **kwargs):
        super(EndpointBaseIntegrationTest, self).__init__(*args, **kwargs)
        self.endpoint_kwargs = {
            'host': os.environ['HOST'],
            'port': os.environ['PORT'],
            'user_id': os.environ['USER_ID'],
            'auth_token': os.environ['AUTH_TOKEN'],
            'secure': os.environ.get('SECURE', 'False').lower() == 'true',
            'version': os.environ.get('VERSION', 'v1')
        }
