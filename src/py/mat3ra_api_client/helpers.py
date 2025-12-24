"""
Helper functions for simplified API interactions.

This module provides convenient wrappers around the endpoint classes
with automatic OIDC authentication support.
"""

import os
from typing import Any, Dict, List, Optional

import requests

from .endpoints.jobs import JobEndpoints
from .endpoints.materials import MaterialEndpoints
from .endpoints.projects import ProjectEndpoints
from .endpoints.workflows import WorkflowEndpoints

# Configuration - can be overridden by environment variables
ACCESS_TOKEN_ENV_VAR = os.getenv("ACCESS_TOKEN_ENV_VAR", "OIDC_ACCESS_TOKEN")
ACCOUNT_ID_ENV_VAR = os.getenv("ACCOUNT_ID_ENV_VAR", "ACCOUNT_ID")


class Endpoints:
    def __init__(self, material, workflow, job, project):
        self.material = material
        self.workflow = workflow
        self.job = job
        self.project = project


def _create_endpoints_with_auth(
    host: str,
    port: int,
    account_id: str,
    auth_token: str,
    version: str = "2018-10-01",
    secure: bool = True,
) -> Endpoints:
    """
    Create endpoint instances with automatic OIDC authentication if available.

    Args:
        host: API host
        port: API port
        account_id: Account ID (can be placeholder if using OIDC)
        auth_token: Legacy auth token (can be placeholder if using OIDC)
        version: API version
        secure: Whether to use HTTPS

    Returns:
        Endpoints instance with all endpoint objects
    """
    endpoint_args = [host, port, account_id, auth_token, version, secure]

    material_endpoints = MaterialEndpoints(*endpoint_args)
    workflow_endpoints = WorkflowEndpoints(*endpoint_args)
    job_endpoints = JobEndpoints(*endpoint_args)
    project_endpoints = ProjectEndpoints(*endpoint_args)

    # Check if OIDC token is available and use it instead of legacy auth
    access_token = os.environ.get(ACCESS_TOKEN_ENV_VAR)
    if access_token:
        auth_header = {"Authorization": f"Bearer {access_token}"}
        material_endpoints.headers.update(auth_header)
        workflow_endpoints.headers.update(auth_header)
        job_endpoints.headers.update(auth_header)
        project_endpoints.headers.update(auth_header)

    return Endpoints(material_endpoints, workflow_endpoints, job_endpoints, project_endpoints)


def get_owner_id(
    endpoints: Endpoints,
    host: str,
    port: int,
    secure: bool = True,
    fallback_account_id: Optional[str] = None,
) -> str:
    """
    Get the owner/account ID, fetching from API if OIDC token is available.

    Args:
        endpoints: Endpoints instance
        host: API host
        port: API port
        secure: Whether to use HTTPS
        fallback_account_id: Fallback account ID if OIDC not available

    Returns:
        Account ID string
    """
    access_token = os.environ.get(ACCESS_TOKEN_ENV_VAR)
    if access_token:
        protocol = "https" if secure else "http"
        port_str = f":{port}" if port not in [80, 443] else ""
        url = f"{protocol}://{host}{port_str}/api/v1/users/me"

        response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
        response.raise_for_status()
        account_id = response.json()["data"]["user"]["entity"]["defaultAccountId"]

        # Cache it for future use
        os.environ[ACCOUNT_ID_ENV_VAR] = account_id
        return account_id

    # Fallback to environment or provided account ID
    account_id = os.environ.get(ACCOUNT_ID_ENV_VAR) or fallback_account_id
    if not account_id or account_id == "ACCOUNT_ID":
        raise ValueError(
            f"{ACCOUNT_ID_ENV_VAR} is not set. Please authenticate first or provide account_id"
        )
    return account_id


def get_material(endpoints: Endpoints, material_id: str) -> Dict[str, Any]:
    return endpoints.material.get(material_id)


def list_materials(
    endpoints: Endpoints,
    query: Optional[Dict[str, Any]] = None,
    owner_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    query_params = query or {}
    if owner_id and "owner._id" not in query_params:
        query_params["owner._id"] = owner_id
    return endpoints.material.list(query_params)


def create_material(
    endpoints: Endpoints,
    material: Any,
    owner_id: str,
) -> Dict[str, Any]:
    raw_config = material.to_dict()
    fields = ["name", "lattice", "basis"]
    config = {key: raw_config[key] for key in fields}
    return endpoints.material.create(config, owner_id)


def get_workflow(endpoints: Endpoints, workflow_id: str) -> Dict[str, Any]:
    return endpoints.workflow.get(workflow_id)


def list_workflows(
    endpoints: Endpoints,
    query: Optional[Dict[str, Any]] = None,
    owner_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    query_params = query or {}
    if owner_id and "owner._id" not in query_params:
        query_params["owner._id"] = owner_id
    return endpoints.workflow.list(query_params)


def create_workflow(
    endpoints: Endpoints,
    workflow: Any,
    owner_id: str,
) -> Dict[str, Any]:
    config = workflow.to_dict()
    return endpoints.workflow.create(config, owner_id)


def get_job(endpoints: Endpoints, job_id: str) -> Dict[str, Any]:
    return endpoints.job.get(job_id)


def list_jobs(
    endpoints: Endpoints,
    query: Optional[Dict[str, Any]] = None,
    owner_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    query_params = query or {}
    if owner_id and "owner._id" not in query_params:
        query_params["owner._id"] = owner_id
    return endpoints.job.list(query_params)


def create_job(
    endpoints: Endpoints,
    materials: List[str],
    workflow_id: str,
    project_id: str,
    name: str,
    compute: Dict[str, Any],
    owner_id: str,
) -> Dict[str, Any]:
    return endpoints.job.create_by_ids(
        materials=materials,
        workflow_id=workflow_id,
        project_id=project_id,
        owner_id=owner_id,
        prefix=name,
        compute=compute,
    )


def get_compute_config(endpoints: Endpoints, cluster: str = "cluster-001") -> Dict[str, Any]:
    return endpoints.job.get_compute(cluster=cluster)


def submit_job(endpoints: Endpoints, job_id: str) -> Dict[str, Any]:
    return endpoints.job.submit(job_id)

def get_default_project(
    endpoints: Endpoints,
    owner_id: str,
) -> str:
    projects = endpoints.project.list({"isDefault": True, "owner._id": owner_id})

    if not projects:
        raise Exception(f"No default project found for owner {owner_id}")

    return projects[0]["_id"]
