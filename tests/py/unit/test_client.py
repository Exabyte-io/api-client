import os
from unittest import mock

from mat3ra.api_client import APIClient

from tests.py.unit import EndpointBaseUnitTest

API_HOST = "platform.mat3ra.com"
API_PORT = "4000"
API_VERSION = "2018-10-01"
API_SECURE_FALSE = "false"

OIDC_ACCESS_TOKEN = "oidc-access-token"
AUTH_TOKEN = "legacy-auth-token"
ACCOUNT_ID = "ubxMkAyx37Rjn8qK9"

ME_ACCOUNT_ID = "my-account-id"
USERS_ME_RESPONSE = {"data": {"user": {"entity": {"defaultAccountId": ME_ACCOUNT_ID}}}}


class APIClientUnitTest(EndpointBaseUnitTest):
    def _base_env(self):
        return {
            "API_HOST": API_HOST,
            "API_PORT": API_PORT,
            "API_VERSION": API_VERSION,
            "API_SECURE": API_SECURE_FALSE,
        }

    def _mock_users_me(self, mock_get):
        mock_resp = mock.Mock()
        mock_resp.json.return_value = USERS_ME_RESPONSE
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

    def test_authenticate_requires_auth(self):
        env = self._base_env()
        with mock.patch.dict("os.environ", env, clear=True):
            with self.assertRaises(ValueError):
                APIClient.authenticate()

    def test_authenticate_oidc_builds_client(self):
        env = self._base_env() | {"OIDC_ACCESS_TOKEN": OIDC_ACCESS_TOKEN}
        with mock.patch.dict("os.environ", env, clear=True):
            client = APIClient.authenticate()
        self.assertEqual(client.host, API_HOST)
        self.assertEqual(client.port, int(API_PORT))
        self.assertEqual(client.version, API_VERSION)
        self.assertFalse(client.secure)
        self.assertTrue(hasattr(client, "materials"))
        self.assertTrue(hasattr(client, "my_account"))

    @mock.patch("requests.get")
    def test_my_account_id_uses_existing_account_id(self, mock_get):
        env = self._base_env() | {"ACCOUNT_ID": ACCOUNT_ID, "AUTH_TOKEN": AUTH_TOKEN}
        with mock.patch.dict("os.environ", env, clear=True):
            client = APIClient.authenticate()
            self.assertEqual(client.my_account.id, ACCOUNT_ID)
        mock_get.assert_not_called()

    @mock.patch("requests.get")
    def test_my_account_id_fetches_and_caches(self, mock_get):
        env = self._base_env() | {"OIDC_ACCESS_TOKEN": OIDC_ACCESS_TOKEN}
        with mock.patch.dict("os.environ", env, clear=True):
            self._mock_users_me(mock_get)
            client = APIClient.authenticate()
            self.assertEqual(client.my_account.id, ME_ACCOUNT_ID)
            self.assertEqual(client.my_account.id, ME_ACCOUNT_ID)
            self.assertEqual(mock_get.call_count, 1)
            self.assertTrue(mock_get.call_args[0][0].endswith("/api/v1/users/me"))
            self.assertEqual(mock_get.call_args[1]["headers"]["Authorization"], f"Bearer {OIDC_ACCESS_TOKEN}")
            self.assertEqual(mock_get.call_args[1]["timeout"], 30)
            self.assertEqual(os.environ.get("ACCOUNT_ID"), ME_ACCOUNT_ID)
