import os
import time

from tests import EndpointBaseTest


class BaseIntegrationTest(EndpointBaseTest):
    """
    Base class for endpoints integration tests.
    """

    def setUp(self) -> None:
        """Add a wait to check for rate limit."""
        time.sleep(2)

    def __init__(self, *args, **kwargs):
        super(BaseIntegrationTest, self).__init__(*args, **kwargs)
        self.endpoint_kwargs = {
            "host": os.environ["TEST_HOST"],
            "port": os.environ["TEST_PORT"],
            "account_id": os.environ["TEST_ACCOUNT_ID"],
            "auth_token": os.environ["TEST_AUTH_TOKEN"],
            "secure": os.environ.get("TEST_SECURE", "False").lower() == "true",
            "version": os.environ.get("TEST_VERSION", "2018-10-01"),
        }

    def tearDown(self) -> None:
        """Delete all created test entities."""
        pass
