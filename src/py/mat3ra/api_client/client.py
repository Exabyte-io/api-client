import os
import re
from typing import Any, List, Optional, Tuple

import requests
from pydantic import BaseModel, ConfigDict

from .constants import ACCESS_TOKEN_ENV_VAR
from .endpoints.bank_materials import BankMaterialEndpoints
from .endpoints.bank_workflows import BankWorkflowEndpoints
from .endpoints.jobs import JobEndpoints
from .endpoints.materials import MaterialEndpoints
from .endpoints.metaproperties import MetaPropertiesEndpoints
from .endpoints.projects import ProjectEndpoints
from .endpoints.properties import PropertiesEndpoints
from .endpoints.workflows import WorkflowEndpoints
from .models import Account, APIEnv, AuthContext, AuthEnv


class APIClient(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow", validate_assignment=True)

    host: str
    port: int
    version: str
    secure: bool
    auth: AuthContext
    timeout_seconds: int = 60

    def model_post_init(self, __context: Any) -> None:
        self.my_account = Account(client=self)
        self.account = self.my_account
        self._my_organization: Optional[Account] = None
        self._init_endpoints(self.timeout_seconds)

    @property
    def my_organization(self) -> Optional[Account]:
        if self._my_organization is None:
            self._my_organization = self.get_default_organization()
        return self._my_organization

    @classmethod
    def env(cls) -> APIEnv:
        return APIEnv.from_env()

    @classmethod
    def auth_env(cls) -> AuthEnv:
        return AuthEnv.from_env()

    def _init_endpoints(self, timeout_seconds: int) -> None:
        kwargs = {"timeout": timeout_seconds, "auth": self.auth}
        account_id = self.auth.account_id or ""
        auth_token = self.auth.auth_token or ""
        self._init_core_endpoints(kwargs, account_id, auth_token)
        self._init_bank_endpoints(kwargs, account_id, auth_token)

    def _init_core_endpoints(self, kwargs: dict, account_id: str, auth_token: str) -> None:
        self.materials = MaterialEndpoints(
            self.host, self.port, account_id, auth_token, version=self.version, secure=self.secure, **kwargs
        )
        self.workflows = WorkflowEndpoints(
            self.host, self.port, account_id, auth_token, version=self.version, secure=self.secure, **kwargs
        )
        self.jobs = JobEndpoints(
            self.host, self.port, account_id, auth_token, version=self.version, secure=self.secure, **kwargs
        )
        self.projects = ProjectEndpoints(
            self.host, self.port, account_id, auth_token, version=self.version, secure=self.secure, **kwargs
        )
        self.properties = PropertiesEndpoints(
            self.host, self.port, account_id, auth_token, version=self.version, secure=self.secure, **kwargs
        )
        self.metaproperties = MetaPropertiesEndpoints(
            self.host, self.port, account_id, auth_token, version=self.version, secure=self.secure, **kwargs
        )

    def _init_bank_endpoints(self, kwargs: dict, account_id: str, auth_token: str) -> None:
        self.bank_materials = BankMaterialEndpoints(
            self.host, self.port, account_id, auth_token, version=self.version, secure=self.secure, **kwargs
        )
        self.bank_workflows = BankWorkflowEndpoints(
            self.host, self.port, account_id, auth_token, version=self.version, secure=self.secure, **kwargs
        )

    @staticmethod
    def _resolve_config(
            host: Optional[str],
            port: Optional[int],
            version: Optional[str],
            secure: Optional[bool],
            env: APIEnv,
    ) -> Tuple[str, int, str, bool]:
        return (
            host if host is not None else env.host,
            port if port is not None else env.port,
            version if version is not None else env.version,
            secure if secure is not None else env.secure,
        )

    @classmethod
    def _auth_from_env(
            cls,
            *,
            access_token: Optional[str],
            account_id: Optional[str],
            auth_token: Optional[str],
    ) -> AuthContext:
        env = cls.auth_env()
        return AuthContext(
            access_token=access_token if access_token is not None else env.access_token,
            account_id=account_id if account_id is not None else env.account_id,
            auth_token=auth_token if auth_token is not None else env.auth_token,
        )

    @staticmethod
    def _validate_auth(auth: AuthContext) -> None:
        if auth.access_token:
            return
        if auth.account_id and auth.auth_token:
            return
        raise ValueError("Missing auth. Provide OIDC_ACCESS_TOKEN or ACCOUNT_ID and AUTH_TOKEN.")

    @classmethod
    def authenticate(
            cls,
            *,
            host: Optional[str] = None,
            port: Optional[int] = None,
            version: Optional[str] = None,
            secure: Optional[bool] = None,
            access_token: Optional[str] = None,
            account_id: Optional[str] = None,
            auth_token: Optional[str] = None,
            timeout_seconds: int = 60,
    ) -> "APIClient":
        host_value, port_value, version_value, secure_value = cls._resolve_config(host, port, version, secure,
                                                                                  cls.env())
        auth = cls._auth_from_env(access_token=access_token, account_id=account_id, auth_token=auth_token)
        cls._validate_auth(auth)
        return cls(host=host_value, port=port_value, version=version_value, secure=secure_value, auth=auth,
                   timeout_seconds=timeout_seconds)

    def _fetch_user_accounts(self) -> List[dict]:
        access_token = self.auth.access_token or os.environ.get(ACCESS_TOKEN_ENV_VAR)
        if not access_token:
            raise ValueError("Access token is required to fetch accounts")

        protocol = "https" if self.secure else "http"
        port_str = f":{self.port}" if self.port not in (80, 443) else ""
        url = f"{protocol}://{self.host}{port_str}/api/v1/users/me"

        response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
        response.raise_for_status()
        return response.json()["data"]["user"].get("accounts", [])

    def list_accounts(self) -> List[dict]:
        accounts = self._fetch_user_accounts()
        return [
            {
                "id": acc["entity"]["_id"],
                "name": acc["entity"].get("name", ""),
                "type": acc["entity"].get("type", "user"),
                "isDefault": acc.get("isDefault", False),
            }
            for acc in accounts
        ]

    def get_account(self, name: Optional[str] = None, index: Optional[int] = None) -> Account:
        """Get account by name (partial regex match) or index from the list of user accounts."""
        if name is None and index is None:
            raise ValueError("Either 'name' or 'index' must be provided")

        accounts = self._fetch_user_accounts()

        if index is not None:
            return Account(client=self, id_cache=accounts[index]["entity"]["_id"])

        pattern = re.compile(name, re.IGNORECASE)
        matches = [acc for acc in accounts if pattern.search(acc["entity"].get("name", ""))]

        if not matches:
            raise ValueError(f"No account found matching '{name}'")
        if len(matches) > 1:
            names = [acc["entity"].get("name", "") for acc in matches]
            raise ValueError(f"Multiple accounts match '{name}': {names}")

        return Account(client=self, id_cache=matches[0]["entity"]["_id"])

    def get_default_organization(self) -> Optional[Account]:
        accounts = self._fetch_user_accounts()
        organizations = [acc for acc in accounts if acc["entity"].get("type") == "organization"]

        if not organizations:
            return None

        for org in organizations:
            if org.get("isDefault"):
                return Account(client=self, id_cache=org["entity"]["_id"])

        return Account(client=self, id_cache=organizations[0]["entity"]["_id"])
