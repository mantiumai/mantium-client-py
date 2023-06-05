import os
from typing import Any

import requests
from openapi_client import ApiClient

version = '0.1.0'


def is_none_or_empty(value: str | None) -> bool:
    """Check if a value is None or empty."""
    if value is None:
        return True

    return not (value and value.strip())


class MantiumClient(ApiClient):
    """Custom ApiClient that handles authentication to the Mantium API."""

    def __init__(self, client_id: str = None, client_secret: str = None) -> None:
        """Initialize the ApiClient with the client_id and client_secret."""
        super().__init__()

        self.client_id = client_id or os.getenv('MANTIUM_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('MANTIUM_CLIENT_SECRET')
        self.token_type = None
        self.access_token = None

        self.host = 'https://api2.mantiumai.com'
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
        if self.token_type and self.access_token:
            return f'{self.token_type} {self.access_token}'
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
                content = r.json()
                self.token_type = content['token_type']
                self.access_token = content['access_token']
                return f'{self.token_type} {self.access_token}'

    def call_api(self, *args: Any, **kwargs: Any) -> tuple:
        """Call the API with the given args and kwargs."""
        resource_path, method, path_params, query_params, header_params = args
        kwargs['auth_settings'] = ['oauth2']
        if 'response_types_map' in kwargs:
            del kwargs['response_types_map']
        if '_request_auth' in kwargs:
            del kwargs['_request_auth']
        header_params.update({'Authorization': f'{self.get_token()}'})
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
