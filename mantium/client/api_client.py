import os
from typing import Any

import requests
from openapi_client import ApiClient


def is_none_or_empty(value: str | None) -> bool:
    """Check if a value is None or empty."""
    if value is None:
        return True

    return not (value and value.strip())


ENV = os.getenv('ENV', 'dev')

host_map = {
    'dev': 'http://localhost:8000',
    'aks-staging': 'https://staging-api.sandbox2.mantiumai.com/',
    'aks-production': 'https://api2.mantiumai.com',
}


version = '0.1.0'


class MantiumClient(ApiClient):
    """Custom ApiClient that handles authentication to the Mantium API."""

    def __init__(self, client_id: str = None, client_secret: str = None) -> None:
        """Initialize the ApiClient with the client_id and client_secret."""
        super().__init__()

        self.client_id = client_id or os.getenv('MANTIUM_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('MANTIUM_CLIENT_SECRET')
        self.access_token: str | None = None

        self.host = host_map.get(ENV, 'http://localhost:8000')
        self.client_side_validation = False

    def get_token(self) -> str:
        """Get a token from the Mantium API."""
        if is_none_or_empty(self.client_id) or is_none_or_empty(self.client_secret):
            raise ValueError('Make sure both MANTIUM_USER and MANTIUM_PASSWORD are set in your env vars.')

        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
        body = dict(
            grant_type='client_credentials',
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope='mantium:client',
        )
        if self.access_token is not None:
            return self.access_token
        else:
            r = requests.post(f'{self.host}/oauth/token', data=body, headers=headers)
            if r.status_code == 403:
                raise ValueError('Username or password incorrect, or token invalid')
            elif r.status_code == 422:
                raise ValueError('Credentials were unprocessable by the API.')
            elif r.status_code != 200:
                raise Exception(
                    'Unexpected issue while attempting to authenticate to the Mantium API. '
                    'Status Code: ' + str(r.status_code)
                )
            else:
                token_content = r.json()
                self.access_token = f'{token_content["token_type"]} {token_content["access_token"]}'
                return self.access_token

    def select_header_content_type(self, content_types, method, body):
        """Select the correct header content type."""
        return 'application/json'

    def call_api(self, *args: Any, **kwargs: Any) -> tuple:
        """Call the API with the given args and kwargs."""
        resource_path, method, path_params, query_params, header_params = args
        kwargs['auth_settings'] = ['oauth2']
        if 'response_types_map' in kwargs:
            del kwargs['response_types_map']
        if '_request_auth' in kwargs:
            del kwargs['_request_auth']

        access_token = self.get_token()
        header_params.update({'Authorization': f'{access_token}', 'User-Agent': 'mantium-client-py/' + version})
        return super().call_api(
            resource_path,
            method,
            path_params,
            query_params,
            header_params,
            response_type=(list(),),
            _host=self.host,
            **kwargs,
        )