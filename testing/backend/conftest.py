"""
Pytest Configuration and Fixtures for Backend Tests
"""
import pytest
import sys
import os
from pathlib import Path

# Add backend directory to path to import app
# We're in testing/backend, need to go to root/backend
backend_path = Path(__file__).parent.parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from app import app as flask_app, get_db_connection

@pytest.fixture
def app():
    """Create and configure a test Flask app instance"""
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """Create a test client for the Flask app"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner for the Flask app"""
    return app.test_cli_runner()

@pytest.fixture
def db():
    """Get database connection for testing"""
    database = get_db_connection()
    yield database
