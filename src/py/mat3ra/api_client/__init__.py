# ruff: noqa: F401
try:
    from ._version import version as __version__
except ModuleNotFoundError:
    __version__ = None

from mat3ra.api_client.endpoints.bank_materials import BankMaterialEndpoints
from mat3ra.api_client.endpoints.bank_workflows import BankWorkflowEndpoints
from mat3ra.api_client.endpoints.jobs import JobEndpoints
from mat3ra.api_client.endpoints.login import LoginEndpoint
from mat3ra.api_client.endpoints.logout import LogoutEndpoint
from mat3ra.api_client.endpoints.materials import MaterialEndpoints
from mat3ra.api_client.endpoints.metaproperties import MetaPropertiesEndpoints
from mat3ra.api_client.endpoints.projects import ProjectEndpoints
from mat3ra.api_client.endpoints.properties import PropertiesEndpoints
from mat3ra.api_client.endpoints.workflows import WorkflowEndpoints

from mat3ra.api_client.client import APIClient
