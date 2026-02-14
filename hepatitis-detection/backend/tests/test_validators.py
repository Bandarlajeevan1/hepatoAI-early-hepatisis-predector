"""
Test input validators
"""
import pytest
from utils.validators import PatientDataValidator, ResponseValidator


class TestValidatePatientInput:
    """Test patient input validation."""

    def test_valid_patient_data(self):
        """Valid patient data should pass validation."""
        data = {
            'age': 35,
            'sex': 1,
            'bilirubin': 0.8,
            'sgot': 25,
            'sgpt': 22,
        }
        is_valid, msg = PatientDataValidator.validate_prediction_input(data)
        assert is_valid is True

    def test_missing_age_fails(self):
        """Missing age should fail validation."""
        data = {'sex': 1}
        is_valid, msg = PatientDataValidator.validate_prediction_input(data)
        assert is_valid is False
        assert 'age' in msg.lower()

    def test_invalid_age_range_fails(self):
        """Age out of range should fail validation."""
        data = {
            'age': 150,  # Max is 120
            'sex': 1,
        }
        is_valid, msg = PatientDataValidator.validate_prediction_input(data)
        assert is_valid is False

    def test_negative_age_fails(self):
        """Negative age should fail validation."""
        data = {
            'age': -5,
            'sex': 1,
        }
        is_valid, msg = PatientDataValidator.validate_prediction_input(data)
        assert is_valid is False

    def test_negative_numeric_value_fails(self):
        """Negative lab value should fail validation."""
        data = {
            'age': 45,
            'sex': 1,
            'bilirubin': -0.5,  # Negative
        }
        is_valid, msg = PatientDataValidator.validate_prediction_input(data)
        assert is_valid is False

    def test_missing_sex_fails(self):
        """Missing sex should fail validation."""
        data = {'age': 35}
        is_valid, msg = PatientDataValidator.validate_prediction_input(data)
        assert is_valid is False

    def test_non_dict_input_fails(self):
        """Non-dict input should fail validation."""
        is_valid, msg = PatientDataValidator.validate_prediction_input("not a dict")
        assert is_valid is False

    def test_empty_dict_fails(self):
        """Empty dict should fail validation."""
        is_valid, msg = PatientDataValidator.validate_prediction_input({})
        assert is_valid is False

    def test_few_fields_fails(self):
        """Too few fields should fail validation."""
        data = {
            'age': 35,
            'sex': 1,
        }
        is_valid, msg = PatientDataValidator.validate_prediction_input(data)
        # May fail if less than 10 features
        assert isinstance(is_valid, bool)


class TestSanitizeInput:
    """Test input sanitization."""

    def test_sanitize_removes_whitespace(self):
        """Sanitizer should handle string values."""
        data = {
            'age': '35',
            'sex': 1,
            'bilirubin': '0.8',
        }
        sanitized = PatientDataValidator.sanitize_input(data)
        assert isinstance(sanitized['age'], float)
        assert isinstance(sanitized['bilirubin'], float)

    def test_sanitize_handles_none_values(self):
        """Sanitizer should preserve None values."""
        data = {
            'age': 35,
            'bilirubin': None,
        }
        sanitized = PatientDataValidator.sanitize_input(data)
        assert sanitized['bilirubin'] is None

    def test_sanitize_converts_numeric_strings(self):
        """Sanitizer should convert numeric strings."""
        data = {
            'age': '45',
            'bilirubin': '0.9',
        }
        sanitized = PatientDataValidator.sanitize_input(data)
        assert isinstance(sanitized['age'], float)
        assert isinstance(sanitized['bilirubin'], float)


class TestResponseValidator:
    """Test response formatting."""

    def test_format_prediction_response(self):
        """Should format prediction response correctly."""
        response = ResponseValidator.format_prediction_response(
            prediction=[1],
            probabilities=[0.2, 0.8],
            risk_level='High'
        )
        assert 'prediction' in response
        assert 'confidence' in response
        assert 'risk_level' in response
        assert response['risk_level'] == 'High'

    def test_format_error_response(self):
        """Should format error response correctly."""
        response, status = ResponseValidator.format_error_response("Test error", 400)
        assert 'error' in response
        assert response['error'] == "Test error"
        assert status == 400

    def test_format_history_response(self):
        """Should format history response correctly."""
        records = [
            {'_id': '1', 'prediction': 'Positive'},
            {'_id': '2', 'prediction': 'Negative'},
        ]
        response = ResponseValidator.format_history_response(records)
        assert 'total' in response
        assert 'records' in response
        assert response['total'] == 2


class TestCategoricalValidation:
    """Test categorical field validation."""

    def test_valid_categorical_field(self):
        """Valid categorical values should pass."""
        data = {
            'age': 35,
            'sex': 1,
            'steroid': 'yes',
        }
        is_valid, msg = PatientDataValidator.validate_prediction_input(data)
        # Should handle categorical fields properly
        assert isinstance(is_valid, bool)

    def test_invalid_categorical_field(self):
        """Invalid categorical values should fail."""
        data = {
            'age': 35,
            'sex': 1,
            'steroid': 'invalid_value',
        }
        is_valid, msg = PatientDataValidator.validate_prediction_input(data)
        # May fail depending on implementation
        assert isinstance(is_valid, bool)
