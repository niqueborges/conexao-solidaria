import pytest

@pytest.fixture
def mock_fetch_data(mocker):
    """Mocks the fetch_data utility used across views."""
    return mocker.patch('utils.http.fetch_data')
