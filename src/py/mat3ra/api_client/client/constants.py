# Environment Variable Names - Exported for external use (e.g., api-examples)
ACCESS_TOKEN_ENV_VAR = "OIDC_ACCESS_TOKEN"
ACCOUNT_ID_ENV_VAR = "ACCOUNT_ID"
AUTH_TOKEN_ENV_VAR = "AUTH_TOKEN"

# OIDC Configuration - Exported for external use
CLIENT_ID = "cli-device-client"
SCOPE = "openid profile email"


def _build_base_url(host: str, port: int, secure: bool, path: str) -> str:
    protocol = "https" if secure else "http"
    port_str = f":{port}" if port not in (80, 443) else ""
    return f"{protocol}://{host}{port_str}{path}"


def build_oidc_base_url(host: str, port: int, secure: bool) -> str:
    """Used in api-examples utils."""
    return _build_base_url(host, port, secure, "/oidc")

