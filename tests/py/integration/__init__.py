import os

import pytest

from tests.conftest import EndpointBaseTest

ENV_TEST_HOST = "TEST_HOST"
ENV_TEST_PORT = "TEST_PORT"
ENV_TEST_ACCOUNT_ID = "TEST_ACCOUNT_ID"
ENV_TEST_AUTH_TOKEN = "TEST_AUTH_TOKEN"
ENV_TEST_SECURE = "TEST_SECURE"
ENV_TEST_VERSION = "TEST_VERSION"
DEFAULT_TEST_SECURE = "False"
DEFAULT_TEST_VERSION = "2018-10-01"

REQUIRED_ENV_VARS = [ENV_TEST_HOST, ENV_TEST_PORT, ENV_TEST_ACCOUNT_ID, ENV_TEST_AUTH_TOKEN]
MISSING_ENV_VARS_MESSAGE = (
    "Integration tests require environment variables: TEST_HOST, TEST_PORT, "
    "TEST_ACCOUNT_ID, TEST_AUTH_TOKEN. Set them to run integration tests."
)


def _check_integration_env():
    """Check if required integration test environment variables are set."""
    missing = [var for var in REQUIRED_ENV_VARS if var not in os.environ]
    if missing:
        pytest.skip(f"{MISSING_ENV_VARS_MESSAGE} Missing: {', '.join(missing)}")


class BaseIntegrationTest(EndpointBaseTest):
    """
    Base class for endpoints integration tests.
    """

    def __init__(self, *args, **kwargs):
        super(BaseIntegrationTest, self).__init__(*args, **kwargs)
        _check_integration_env()
        self.endpoint_kwargs = {
            "host": os.environ[ENV_TEST_HOST],
            "port": os.environ[ENV_TEST_PORT],
            "account_id": os.environ[ENV_TEST_ACCOUNT_ID],
            "auth_token": os.environ[ENV_TEST_AUTH_TOKEN],
            "secure": os.environ.get(ENV_TEST_SECURE, DEFAULT_TEST_SECURE).lower() == "true",
            "version": os.environ.get(ENV_TEST_VERSION, DEFAULT_TEST_VERSION),
        }
