import os
from typing import Any, Optional, Tuple

import requests
from pydantic import BaseModel, ConfigDict, Field

from mat3ra.api_client.endpoints.bank_materials import BankMaterialEndpoints
from mat3ra.api_client.endpoints.bank_workflows import BankWorkflowEndpoints
from mat3ra.api_client.endpoints.jobs import JobEndpoints
from mat3ra.api_client.endpoints.materials import MaterialEndpoints
from mat3ra.api_client.endpoints.metaproperties import MetaPropertiesEndpoints
from mat3ra.api_client.endpoints.projects import ProjectEndpoints
from mat3ra.api_client.endpoints.properties import PropertiesEndpoints
from mat3ra.api_client.endpoints.workflows import WorkflowEndpoints

# Default API Configuration
DEFAULT_API_HOST = "platform.mat3ra.com"
DEFAULT_API_PORT = 443
DEFAULT_API_VERSION = "2018-10-01"
DEFAULT_API_SECURE = True

# Environment Variable Names
ACCESS_TOKEN_ENV_VAR = "OIDC_ACCESS_TOKEN"
API_HOST_ENV_VAR = "API_HOST"
API_PORT_ENV_VAR = "API_PORT"
API_VERSION_ENV_VAR = "API_VERSION"
API_SECURE_ENV_VAR = "API_SECURE"
ACCOUNT_ID_ENV_VAR = "ACCOUNT_ID"
AUTH_TOKEN_ENV_VAR = "AUTH_TOKEN"

# Default OIDC Configuration
CLIENT_ID = "default-client"
CLIENT_SECRET = "default-secret"
SCOPE = "openid profile email"

# API Paths
USERS_ME_PATH = "/api/v1/users/me"


class AuthContext(BaseModel):
    access_token: Optional[str] = None
    account_id: Optional[str] = None
    auth_token: Optional[str] = None


class APIEnv(BaseModel):
    host: str = Field(default=DEFAULT_API_HOST, validation_alias=API_HOST_ENV_VAR)
    port: int = Field(default=DEFAULT_API_PORT, validation_alias=API_PORT_ENV_VAR)
    version: str = Field(default=DEFAULT_API_VERSION, validation_alias=API_VERSION_ENV_VAR)
    secure: bool = Field(default=DEFAULT_API_SECURE, validation_alias=API_SECURE_ENV_VAR)

    @classmethod
    def from_env(cls) -> "APIEnv":
        return cls.model_validate(os.environ)


class AuthEnv(BaseModel):
    access_token: Optional[str] = Field(None, validation_alias=ACCESS_TOKEN_ENV_VAR)
    account_id: Optional[str] = Field(None, validation_alias=ACCOUNT_ID_ENV_VAR)
    auth_token: Optional[str] = Field(None, validation_alias=AUTH_TOKEN_ENV_VAR)

    @classmethod
    def from_env(cls) -> "AuthEnv":
        return cls.model_validate(os.environ)


class Account(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    client: Any = Field(exclude=True, repr=False)
    id_cache: Optional[str] = None

    @property
    def id(self) -> str:
        if self.id_cache:
            return self.id_cache
        self.id_cache = self.client._resolve_account_id()
        return self.id_cache


def _build_base_url(host: str, port: int, secure: bool, path: str) -> str:
    protocol = "https" if secure else "http"
    port_str = f":{port}" if port not in (80, 443) else ""
    return f"{protocol}://{host}{port_str}{path}"

# Used in API-examples utils
def build_oidc_base_url(host: str, port: int, secure: bool) -> str:
    return _build_base_url(host, port, secure, "/oidc")

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
        self._init_endpoints(self.timeout_seconds)

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

    def _resolve_account_id(self) -> str:
        account_id = self.auth.account_id or os.environ.get(ACCOUNT_ID_ENV_VAR)
        if account_id:
            self.auth.account_id = account_id
            return account_id

        access_token = self.auth.access_token or os.environ.get(ACCESS_TOKEN_ENV_VAR)
        if not access_token:
            raise ValueError("ACCOUNT_ID is not set and no OIDC access token is available.")

        url = _build_base_url(self.host, self.port, self.secure, USERS_ME_PATH)
        response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
        response.raise_for_status()
        account_id = response.json()["data"]["user"]["entity"]["defaultAccountId"]
        os.environ[ACCOUNT_ID_ENV_VAR] = account_id
        self.auth.account_id = account_id
        return account_id
