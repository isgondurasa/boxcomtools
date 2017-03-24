"""
General fixtures for application testing.
"""
import pytest
import aiohttp

@pytest.fixture
def client(loop, test_client):
    app = aiohttp.web.Application(loop=loop)
    return loop.run_until_complete(test_client(app))
