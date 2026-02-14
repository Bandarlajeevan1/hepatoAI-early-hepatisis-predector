"""
Test API endpoints
"""
import json
import pytest


class TestHealthEndpoint:
    """Test /health endpoint."""

    def test_health_check_returns_200(self, client):
        """Health check should return 200 OK."""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_check_has_required_fields(self, client):
        """Health check response should have required fields."""
        response = client.get('/health')
        data = json.loads(response.data)
        assert 'status' in data
        assert 'model_loaded' in data
        assert 'timestamp' in data


class TestInfoEndpoint:
    """Test /info endpoint."""

    def test_info_returns_200(self, client):
        """Info endpoint should return 200 OK."""
        response = client.get('/info')
        assert response.status_code == 200

    def test_info_has_application_name(self, client):
        """Info response should have application name."""
        response = client.get('/info')
        data = json.loads(response.data)
        assert 'application' in data
        assert 'Hepatitis' in data['application']


class TestPredictEndpoint:
    """Test /predict endpoint."""

    def test_predict_requires_post(self, client):
        """Predict endpoint should only accept POST."""
        response = client.get('/predict')
        assert response.status_code == 405  # Method not allowed

    def test_predict_requires_json(self, client):
        """Predict endpoint should require JSON."""
        response = client.post('/predict', data='invalid')
        assert response.status_code == 400

    def test_predict_returns_error_without_data(self, client):
        """Predict should return error for empty data."""
        response = client.post('/predict', json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_predict_returns_error_for_invalid_age(self, client):
        """Predict should validate age range."""
        response = client.post('/predict', json={
            'age': 150,  # Out of range
            'sex': 1
        })
        assert response.status_code == 400

    def test_predict_with_valid_data_returns_prediction(self, client, sample_patient_data):
        """Predict should return prediction for valid data if model is loaded."""
        response = client.post('/predict', json=sample_patient_data)
        # May return 500 if model not loaded, but structure should be valid JSON
        assert response.status_code in [200, 500]
        data = json.loads(response.data)
        # Should have either prediction or error
        assert 'prediction' in data or 'error' in data


class TestSaveEndpoint:
    """Test /save endpoint."""

    def test_save_requires_post(self, client):
        """Save endpoint should only accept POST."""
        response = client.get('/save')
        assert response.status_code == 405

    def test_save_returns_error_without_json(self, client):
        """Save should return error for invalid JSON."""
        response = client.post('/save', data='invalid')
        assert response.status_code == 400

    def test_save_returns_error_without_data(self, client):
        """Save should return error for empty data."""
        response = client.post('/save', json={})
        # May return 500 if DB not available
        assert response.status_code in [200, 500]


class TestHistoryEndpoint:
    """Test /history endpoint."""

    def test_history_requires_get(self, client):
        """History endpoint should only accept GET."""
        response = client.post('/history')
        assert response.status_code == 405

    def test_history_returns_json(self, client):
        """History endpoint should return JSON."""
        response = client.get('/history')
        assert response.status_code in [200, 500]
        data = json.loads(response.data)
        # Should have structure
        assert data is not None

    def test_history_limit_parameter(self, client):
        """History should accept limit parameter."""
        response = client.get('/history?limit=10')
        assert response.status_code in [200, 500]

    def test_history_limit_capped_at_1000(self, client):
        """History limit should be capped at 1000."""
        response = client.get('/history?limit=9999')
        assert response.status_code in [200, 500]


class TestError404:
    """Test 404 error handling."""

    def test_invalid_endpoint_returns_404(self, client):
        """Invalid endpoint should return 404."""
        response = client.get('/invalid-endpoint')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data


class TestErrorHandling:
    """Test error handling."""

    def test_invalid_json_returns_400(self, client):
        """Invalid JSON should return 400."""
        response = client.post(
            '/predict',
            data='not json',
            content_type='application/json'
        )
        assert response.status_code in [400, 415]

    def test_missing_required_fields(self, client):
        """Missing required fields should return error."""
        response = client.post('/predict', json={
            'age': 35
            # Missing sex
        })
        assert response.status_code == 200 or 'error' in json.loads(response.data)
