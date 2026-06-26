import pytest
from mintzy.client import MintzyClient

@pytest.fixture
def api_key():
    return "sk_test_12345"

@pytest.fixture
def client(api_key):
    with MintzyClient(api_key=api_key, base_url="https://api.mintzy.com") as client:
        yield client
