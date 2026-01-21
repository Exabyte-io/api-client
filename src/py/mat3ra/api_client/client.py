from typing import Any, Optional, Tuple

from pydantic import BaseModel, ConfigDict

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
