import pytest


@pytest.fixture
def required_args():
    return '--user testuser --client_id a --client_secret b'
