# Mantium Client
[![Mantium logo](https://avatars.githubusercontent.com/u/82233875?s=20&v=4)](https://mantiumai.com/)
[![CI status](https://github.com/mantiumai/mantium-client-py/actions/workflows/test.yml/badge.svg)](https://github.com/mantiumai/mantium-client-py/actions)
[![PyPI](https://img.shields.io/pypi/v/mantium-client?color=green)](https://pypi.org/project/mantium-client/)
[![License](https://img.shields.io/github/license/mantiumai/mantium-client-py)](https://github.com/mantiumai/mantium-client-py/blob/main/LICENSE.txt)


A Python client library for [Mantium](https://mantiumai.com/) services.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install this client.

```bash
pip install mantium-client
```

## Usage

```python
from mantium_client.api_client import ApiClient
from mantium_spec.api.applications_api import ApplicationsApi

client = ApiClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
apps_api = ApplicationsApi(api_client=client)

# returns a list of applications
apps_api.list_applications()
```

## License

[Apache-2.0](https://choosealicense.com/licenses/apache-2.0/)

## Development

This is only necessary if you want to develop in this project.

We use `poetry` for dependency management.
```shell
pip install poetry
poetry install --with dev,test --verbose
```
