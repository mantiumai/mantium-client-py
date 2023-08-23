import os
from typing import Any, Optional

import requests
from openapi_client import ApiClient
from openapi_client.exceptions import ForbiddenException, UnauthorizedException
from tenacity import RetryCallState, Retrying, retry_if_exception_type, stop_after_attempt, wait_fixed

from .version import __version__


def is_none_or_empty(value: Optional[str]) -> bool:
    """Check if a value is None or empty."""
    if value is None:
        return True

    return not (value and value.strip())


version = __version__


class MantiumClient(ApiClient):
    """Custom ApiClient that handles authentication to the Mantium API."""

    def __init__(self, client_id: str = None, client_secret: str = None) -> None:
        """Initialize the ApiClient with the client_id and client_secret."""
        super().__init__()

        self.client_id = client_id or os.getenv('MANTIUM_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('MANTIUM_CLIENT_SECRET')
        self.access_token: Optional[str] = None

        self.host = os.getenv('ROOT_URL', 'https://api2.mantiumai.com')
        self.client_side_validation = False

    def get_token(self) -> str:
        """Get a token from the Mantium API."""
        if is_none_or_empty(self.client_id) or is_none_or_empty(self.client_secret):
            raise ValueError('Make sure both MANTIUM_CLIENT_ID and MANTIUM_CLIENT_SECRET are set in your env vars.')

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
                raise ValueError('MANTIUM_CLIENT_ID or MANTIUM_CLIENT_SECRET incorrect, or token invalid')
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

    def select_header_content_type(self, content_types: list, method: str, body: dict) -> str:
        """Select the correct header content type."""
        return 'application/json'

    def _refresh_token(self, _: RetryCallState) -> None:
        """Refresh the token."""
        self.access_token = None
        self.get_token()

    def call_api(self, *args: Any, **kwargs: Any) -> tuple:
        """Call the API with the given args and kwargs."""
        resource_path, method, path_params, query_params, header_params = args
        kwargs['auth_settings'] = ['oauth2']
        if 'response_types_map' in kwargs:
            del kwargs['response_types_map']
        if '_request_auth' in kwargs:
            del kwargs['_request_auth']

        access_token = self.get_token()
        header_params.update({'Authorization': f'{access_token}', 'User-Agent': 'mantium_client-mantium-py/' + version})

        retryer = Retrying(
            reraise=True,
            wait=wait_fixed(2),
            stop=stop_after_attempt(3),
            before_sleep=self._refresh_token,
            retry=retry_if_exception_type((UnauthorizedException, ForbiddenException)),
        )
        for attempt in retryer:
            with attempt:
                response = super().call_api(
                    resource_path,
                    method,
                    path_params,
                    query_params,
                    header_params,
                    response_type=(list(),),
                    _host=self.host,
                    **kwargs,
                )
        return response
