import os

import pytest
from tests.py.conftest import EndpointBaseTest

DEFAULT_TEST_SECURE = "False"
DEFAULT_TEST_VERSION = "2018-10-01"

REQUIRED_ENV_VARS = ["TEST_HOST", "TEST_PORT", "TEST_ACCOUNT_ID", "TEST_AUTH_TOKEN"]


def _check_integration_env():
    """Check if required integration test environment variables are set."""
    missing = [var for var in REQUIRED_ENV_VARS if var not in os.environ]
    if missing:
        pytest.skip("Integration tests require environment variables: TEST_HOST, TEST_PORT, TEST_ACCOUNT_ID, " +
                    f"TEST_AUTH_TOKEN. Set them to run integration tests. Missing: {', '.join(missing)}")


class BaseIntegrationTest(EndpointBaseTest):
    """
    Base class for endpoints integration tests.
    """

    def __init__(self, *args, **kwargs):
        super(BaseIntegrationTest, self).__init__(*args, **kwargs)
        _check_integration_env()
        self.endpoint_kwargs = {
            "host": os.environ["TEST_HOST"],
            "port": os.environ["TEST_PORT"],
            "account_id": os.environ["TEST_ACCOUNT_ID"],
            "auth_token": os.environ["TEST_AUTH_TOKEN"],
            "secure": os.environ.get("TEST_SECURE", DEFAULT_TEST_SECURE).lower() == "true",
            "version": os.environ.get("TEST_VERSION", DEFAULT_TEST_VERSION),
        }
