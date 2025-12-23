import os
from typing import Any, Optional, Tuple

import requests
from pydantic import BaseModel, ConfigDict, Field

from exabyte_api_client.endpoints.bank_materials import BankMaterialEndpoints
from exabyte_api_client.endpoints.bank_workflows import BankWorkflowEndpoints
from exabyte_api_client.endpoints.jobs import JobEndpoints
from exabyte_api_client.endpoints.materials import MaterialEndpoints
from exabyte_api_client.endpoints.metaproperties import MetaPropertiesEndpoints
from exabyte_api_client.endpoints.projects import ProjectEndpoints
from exabyte_api_client.endpoints.properties import PropertiesEndpoints
from exabyte_api_client.endpoints.workflows import WorkflowEndpoints


class AuthContext(BaseModel):
    access_token: Optional[str] = None
    account_id: Optional[str] = None
    auth_token: Optional[str] = None


class APIEnv(BaseModel):
    host: str = Field(validation_alias="API_HOST")
    port: int = Field(validation_alias="API_PORT")
    version: str = Field(validation_alias="API_VERSION")
    secure: bool = Field(validation_alias="API_SECURE")

    @classmethod
    def from_env(cls) -> "APIEnv":
        return cls.model_validate(os.environ)


class AuthEnv(BaseModel):
    access_token: Optional[str] = Field(None, validation_alias="OIDC_ACCESS_TOKEN")
    account_id: Optional[str] = Field(None, validation_alias="ACCOUNT_ID")
    auth_token: Optional[str] = Field(None, validation_alias="AUTH_TOKEN")

    @classmethod
    def from_env(cls) -> "AuthEnv":
        return cls.model_validate(os.environ)


class Account(BaseModel):
    client: Any = Field(exclude=True, repr=False)
    id_cache: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True

    @property
    def id(self) -> str:
        if self.id_cache:
            return self.id_cache
        self.id_cache = self.client._resolve_account_id()
        return self.id_cache


def _build_users_me_url(host: str, port: int, secure: bool) -> str:
    protocol = "https" if secure else "http"
    port_str = f":{port}" if port not in [80, 443] else ""
    return f"{protocol}://{host}{port_str}/api/v1/users/me"


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
        account_id = self.auth.account_id or os.environ.get("ACCOUNT_ID")
        if account_id:
            self.auth.account_id = account_id
            return account_id

        access_token = self.auth.access_token or os.environ.get("OIDC_ACCESS_TOKEN")
        if not access_token:
            raise ValueError("ACCOUNT_ID is not set and no OIDC access token is available.")

        url = _build_users_me_url(self.host, self.port, self.secure)
        response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
        response.raise_for_status()
        account_id = response.json()["data"]["user"]["entity"]["defaultAccountId"]
        os.environ["ACCOUNT_ID"] = account_id
        self.auth.account_id = account_id
        return account_id
