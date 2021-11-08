from app import zonaCipta_app
import logging
import pytest

@pytest.fixture
def app():
    app = zonaCipta_app({'TESTING': True})
    return app
    