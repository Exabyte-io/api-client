[![PyPI version](https://badge.fury.io/py/exabyte-api-client.svg)](https://badge.fury.io/py/exabyte-api-client)

This package provides access to Exabyte.io [RESTful API](https://docs.mat3ra.com/rest-api/overview/).

# Installation

We recommend creating a virtual environment before installing:

```bash
virtualenv my-virtualenv
source my-virtualenv/bin/activate
```

Install using pip:

- from PyPI:

```bash
pip install exabyte-api-client
```

- from source code in development mode:

```bash
git clone git@github.com:Exabyte-io/exabyte-api-client.git
cd exabyte-api-client
pip install -e .
```

# Examples

[exabyte-api-examples](https://github.com/Exabyte-io/exabyte-api-examples) repository contains examples for performing most-common tasks in the Exabyte.io platform through its RESTful API in Jupyter Notebook format.

# Testing
A Virtualenv environment can be created and the tests run with the included `run-tests.sh` script.
To run the unit tests in Python 3, you can:
```
./run-tests -t=unit
```

To run the integration tests in Python 2, you can:
```
./run-tests -p=python2 -t=integration
```
(assuming you have a `python2` binary in your PATH environment).

Note that the integration tests require a REST API service against which the live tests will run. See `tests/integration/__init__.py` for the environment variable details.


© 2020 Exabyte Inc.
