from unittest.mock import patch

import pytest
from mantium_spec import ApplicationsApi

from mantium_client.api_client import MantiumClient


@pytest.fixture
def client():
    client_id = 'test_client_id'
    client_secret = 'test_client_secret'

    client = MantiumClient(client_id, client_secret)

    assert client.client_id == client_id
    assert client.client_secret == client_secret

    return client


def test_get_token(client):
    with patch('mantium_client.api_client.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = dict(access_token='test_token', token_type='Bearer')

        token = client.get_token()

    assert token.startswith('Bearer ')


def test_call_api(client):
    """Test the call_api method of the MantiumClient class."""
    mock_requests_post_target = 'mantium_client.api_client.requests.post'
    mock_call_api_target = 'mantium_client.api_client.ApiClient.call_api'
    with patch(mock_requests_post_target) as mock_post, patch(mock_call_api_target) as mock_call_api:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = dict(
            access_token='test_token', token_type='Bearer', expires_in=3600, scope='test_scope'
        )

        mock_call_api.return_value = 'test_response'

        client.call_api('test_path', 'GET', [], {'test_header': 'test'}, {'test_data': 'foo'})

    mock_call_api.assert_called_once()
    args, kwargs = mock_call_api.call_args
    assert args[0] == 'test_path'
    assert args[1] == 'GET'
    assert args[3] == {'test_header': 'test'}
    assert args[4] == {
        'test_data': 'foo',
        'Authorization': 'Bearer test_token',
        'User-Agent': 'mantium_client-mantium-py/0.1.0',
    }


def test_list_applications(client):
    apps_api = ApplicationsApi(client)
    mock_requests_post_target = 'mantium_client.api_client.requests.post'
    mock_call_api_target = 'mantium_client.api_client.ApiClient.call_api'
    with patch(mock_requests_post_target) as mock_post, patch(mock_call_api_target) as mock_call_api:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = dict(
            access_token='test_token', token_type='Bearer', expires_in=3600, scope='test_scope'
        )
        mock_call_api.return_value = dict(detail=[], count=0, next=None, previous=None)

        apps_api.list_applications()

    mock_call_api.assert_called_once()
    args, kwargs = mock_call_api.call_args
    assert args[0] == '/applications/'
    assert args[1] == 'GET'
