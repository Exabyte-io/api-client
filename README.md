[![PyPI version](https://badge.fury.io/py/mat3ra-api-client.svg)](https://badge.fury.io/py/mat3ra-api-client)

This package provides access to Mat3ra.com [RESTful API](https://docs.mat3ra.com/rest-api/overview/).

# Installation

We recommend creating a virtual environment before installing:

```bash
virtualenv my-virtualenv
source my-virtualenv/bin/activate
```

Install using pip:

- from PyPI:

```bash
pip install mat3ra-api-client
```

- from source code in development mode:

```bash
git clone git@github.com:Exabyte-io/api-client.git
cd api-client
pip install -e .
```

# Usage

```python
from mat3ra.api_client import APIClient

# Authenticate with OIDC token
client = APIClient.authenticate()

# Access endpoints
materials = client.materials.list()
```

# Examples

[api-examples](https://github.com/Exabyte-io/api-examples) repository contains examples for performing most-common tasks in the Mat3ra.com platform through its RESTful API in Jupyter Notebook format.

# Testing

The package uses pytest for testing. Tests are organized into unit and integration tests.

## Running Tests

### Unit Tests (No environment setup required)

Run all unit tests:
```bash
pytest tests/py/unit
```

### Integration Tests (Requires API credentials)

Integration tests require the following environment variables to be set:

- `TEST_HOST` - API host (e.g., `platform.mat3ra.com`)
- `TEST_PORT` - API port (e.g., `443`)
- `TEST_ACCOUNT_ID` - Your account ID
- `TEST_AUTH_TOKEN` - Your authentication token
- `TEST_SECURE` - Use HTTPS (optional, default: `False`)
- `TEST_VERSION` - API version (optional, default: `2018-10-01`)

To run integration tests:
```bash
export TEST_HOST=platform.mat3ra.com
export TEST_PORT=443
export TEST_ACCOUNT_ID=your-account-id
export TEST_AUTH_TOKEN=your-auth-token
export TEST_SECURE=true

pytest tests/py/integration
```

### Run All Tests

```bash
pytest tests/py
```

### Run Tests with Coverage

```bash
pytest tests/py/unit --cov=mat3ra.api_client --cov-report=term --cov-report=html
```

**Note:** Integration tests will be automatically skipped if required environment variables are not set.


© 2020 Exabyte Inc.
