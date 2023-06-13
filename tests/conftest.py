import pytest


@pytest.fixture(autouse=True)
def no_http_requests(monkeypatch, request):
    """
    Do not allow tests to make network requests.

    This works for most http request libraries.
    """

    def urlopen_mock(self, method, url, *args, **kwargs):
        raise RuntimeError(f'The test was about to {method} {self.scheme}://{self.host}{url}')

    # Only use this for unit tests. Integration tests should be allowed to reach out to the network.
    if 'integration' not in request.keywords:
        monkeypatch.setattr('urllib3.connectionpool.HTTPConnectionPool.urlopen', urlopen_mock)
        yield
        monkeypatch.undo()
    else:
        print('No http request blocking')
        yield
