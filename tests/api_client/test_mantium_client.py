from unittest.mock import patch

import pytest

from mantium.client.api_client import MantiumClient


@pytest.fixture
def client():
    client_id = 'test_client_id'
    client_secret = 'test_client_secret'

    client = MantiumClient(client_id, client_secret)

    assert client.client_id == client_id
    assert client.client_secret == client_secret

    return client


def test_get_token(client):
    with patch('mantium.client.api_client.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = dict(access_token='test_token', token_type='Bearer')

        token = client.get_token()

    assert token.startswith('Bearer ')
