# Mantium Client
[![Mantium logo](https://avatars.githubusercontent.com/u/82233875?s=20&v=4)](https://mantiumai.com/)
[![CI status](https://github.com/mantiumai/mantium-client-py/actions/workflows/test.yml/badge.svg)](https://github.com/mantiumai/mantium-client-py/actions)
[![PyPI](https://img.shields.io/pypi/v/mantium-client?color=green)](https://pypi.org/project/mantium-client/)
[![License](https://img.shields.io/github/license/mantiumai/mantium-client-py)](https://github.com/mantiumai/mantium-client-py/blob/main/LICENSE.txt)


A Python client library for [Mantium](https://mantiumai.com/) services.

## Prerequisites

Before you start working with this client, there are a few steps you need to complete. These prerequisites will help ensure that you can seamlessly interact with Mantium's functionalities.

### 1. Request Beta Access

Firstly, you need to sign up for beta access. 
Visit the [Mantium Beta Signup](https://mantiumai.com/beta-signup/) page, 
fill in the necessary details, and submit your form to request beta access. 
Once your request has been approved, you'll be granted access to create an account 
and explore Mantium's extensive range of features.

### 2. Create an Application

After creating an account and logging in, your next step is to create an application. 
Mantium offers a variety of pre-made templates to simplify this process. 
For example, you might choose the Recipe Management template. 

When you create an application from a pre-made template, two key steps will occur:

1. You will upload files or connect to a data source such as Notion or Slack. This is where the application will pull content from.
2. The content provided by you will be pre-processed, vectorized, and then stored in a Redis vector database.

After performing these steps, you can engage with your data in a meaningful way through the application you've just created.

### 3. Enable API Access

From your dashboard or main menu, locate and click on the User Profile section.

Within your user profile, there's an option to enable Python Client Access. This step is vital as it unlocks the interface that the client will use to communicate with your application:

![User Profile Navigation](https://github.com/mantiumai/mantium-client-py/assets/48630278/ad386890-44d1-42fc-b229-f16ae9aa3e78)

### 4. Client ID and Client Secret

Upon enabling API access, Mantium will present a Client ID and Client Secret. These unique identifiers authenticate your client's requests to the Mantium application. Please record them carefully. You will need to use them with the MantiumClient, as shown in the Usage section below.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install this client.

```bash
pip install mantium-client
```

## Usage

```python
from mantium_spec.api.applications_api import ApplicationsApi
from mantium_client.api_client import MantiumClient

client = MantiumClient(client_id=client_id, client_secret=client_secret)
apps_api = ApplicationsApi(client)

# returns a list of applications
apps_api.list_applications()

# returns an application's details
apps_api.get_application_detail(application_id)

# query an application
query_request = {'query': 'What should I have for dinner tonight?'}
return apps_api.query_application(application_id, query_request)
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
