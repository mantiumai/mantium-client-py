# Mantium Client

![CI status](https://github.com/mantiumai/mantium-client-py/actions/workflows/test.yml/badge.svg?branch=main)

A Python client library for [Mantium services](https://mantiumai.com/).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install this client.

```bash
pip install mantium
```

## Usage

```python
from mantium import ApiClient
from mantium.openapi_client.api.applications_api import ApplicationsApi


client = ApiClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
apps_api = ApplicationsApi(api_client=client)

# returns a list of applications
apps_api.list_applications()
```

## License

[Apache-2.0](https://choosealicense.com/licenses/apache-2.0/)

## Development

We use `poetry` for dependency management.
```shell
pip install poetry
poetry install
```
