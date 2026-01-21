import os
from typing import Any, Optional

import requests
from pydantic import BaseModel, ConfigDict, Field

from .constants import ACCESS_TOKEN_ENV_VAR, ACCOUNT_ID_ENV_VAR, AUTH_TOKEN_ENV_VAR, _build_base_url


class AuthContext(BaseModel):
    access_token: Optional[str] = None
    account_id: Optional[str] = None
    auth_token: Optional[str] = None


class APIEnv(BaseModel):
    host: str = Field(default="platform-new.mat3ra.com", validation_alias="API_HOST")
    port: int = Field(default=443, validation_alias="API_PORT")
    version: str = Field(default="2018-10-01", validation_alias="API_VERSION")
    secure: bool = Field(default=True, validation_alias="API_SECURE")

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
        self.id_cache = self._resolve_account_id()
        return self.id_cache

    def _resolve_account_id(self) -> str:
        account_id = self.client.auth.account_id or os.environ.get(ACCOUNT_ID_ENV_VAR)
        if account_id:
            self.client.auth.account_id = account_id
            return account_id

        access_token = self.client.auth.access_token or os.environ.get(ACCESS_TOKEN_ENV_VAR)
        if not access_token:
            raise ValueError("ACCOUNT_ID is not set and no OIDC access token is available.")

        url = _build_base_url(self.client.host, self.client.port, self.client.secure, "/api/v1/users/me")
        response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
        response.raise_for_status()
        account_id = response.json()["data"]["user"]["entity"]["defaultAccountId"]
        os.environ[ACCOUNT_ID_ENV_VAR] = account_id
        self.client.auth.account_id = account_id
        return account_id

