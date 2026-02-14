"""
Pytest configuration and fixtures
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import mongomock

# Set environment variables for testing
os.environ['FLASK_ENV'] = 'testing'
os.environ['MONGO_URI'] = 'mongodb://mongomock/'


@pytest.fixture
def app():
    """Create Flask app for testing."""
    from app import app
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create Flask test client."""
    return app.test_client()


@pytest.fixture
def sample_patient_data():
    """Sample patient data for testing."""
    return {
        'age': 45,
        'sex': 1,
        'steroid': 1,
        'antivirals': 1,
        'fatigue': 1,
        'malaise': 1,
        'anorexia': 1,
        'liver_big': 1,
        'liver_firm': 1,
        'spleen_palpable': 0,
        'spider_web': 0,
        'ascites': 0,
        'varices': 0,
        'bilirubin': 0.8,
        'alk_phosphatase': 66,
        'sgot': 28,
        'sgpt': 25,
        'albumin': 4.0,
        'protime': 20,
    }


@pytest.fixture
def sample_invalid_patient_data():
    """Invalid patient data for testing."""
    return {
        'age': 150,  # Invalid age
        'sex': 1,
        'bilirubin': -5,  # Negative value
    }
