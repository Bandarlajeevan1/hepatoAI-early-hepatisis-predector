"""
Input validation for patient data and API requests.
"""
from typing import Dict, Tuple, List, Any
from utils.constants import (
    HEPATITIS_FEATURES,
    ILPD_FEATURES,
    CATEGORICAL_FEATURES,
    FEATURE_RANGES,
    ERROR_MISSING_FIELDS,
    ERROR_INVALID_INPUT,
)


class PatientDataValidator:
    """Validate patient data for prediction."""

    @staticmethod
    def validate_prediction_input(data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate patient data for prediction endpoint.

        Args:
            data: Dictionary containing patient features

        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if not isinstance(data, dict):
            return False, "Input must be a JSON dictionary"

        if not data:
            return False, ERROR_MISSING_FIELDS

        # Check for required fields (at least hepatitis core features)
        # Allow flexible feature sets (either hepatitis or ILPD)
        required_fields = set(HEPATITIS_FEATURES) | set(ILPD_FEATURES)
        provided_fields = set(data.keys())

        # At least 10 features should be provided
        if len(provided_fields) < 10:
            return False, f"Provide at least 10 features. Got {len(provided_fields)}"

        # Validate data types and ranges
        for field, value in data.items():
            # Check if value is numeric (int/float) or categorical string
            if isinstance(value, str):
                # Allow categorical values
                if field in CATEGORICAL_FEATURES:
                    if value.lower() not in ["yes", "no", "male", "female", "1", "0"]:
                        return (
                            False,
                            f"Invalid categorical value for {field}: {value}",
                        )
                else:
                    return False, f"Field {field} should be numeric, got string: {value}"
            elif isinstance(value, (int, float)):
                # Validate numeric ranges if defined
                if field in FEATURE_RANGES:
                    min_val, max_val = FEATURE_RANGES[field]
                    if not (min_val <= value <= max_val):
                        return (
                            False,
                            f"Value for {field} out of range [{min_val}, {max_val}]: {value}",
                        )
            elif value is None:
                # None values are acceptable (for imputation)
                pass
            else:
                return False, f"Invalid type for field {field}: {type(value)}"

        return True, "Validation passed"

    @staticmethod
    def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize patient data: convert types, handle missing values.

        Args:
            data: Raw patient data

        Returns:
            Sanitized dictionary
        """
        sanitized = {}

        for key, value in data.items():
            # Skip None values (will be imputed)
            if value is None:
                sanitized[key] = None
            # Convert string numbers to float
            elif isinstance(value, str):
                try:
                    sanitized[key] = float(value)
                except ValueError:
                    # Keep as string for categorical
                    sanitized[key] = value.lower().strip()
            else:
                sanitized[key] = float(value) if isinstance(value, (int, float)) else value

        return sanitized


class ResponseValidator:
    """Validate and format API responses."""

    @staticmethod
    def format_prediction_response(
        prediction: List[int],
        probabilities: Any,
        risk_level: str,
        patient_id: str = None,
    ) -> Dict[str, Any]:
        """
        Format prediction response for API.

        Args:
            prediction: Predicted class (array with single element)
            probabilities: Probability score(s) - can be scalar (positive class only) or array [neg, pos]
            risk_level: Risk level ("Low", "Medium", "High")
            patient_id: Optional patient identifier

        Returns:
            Formatted response dictionary
        """
        import numpy as np
        
        # Convert prediction to scalar if needed
        if isinstance(prediction, (np.ndarray, list)):
            pred_value = int(prediction[0]) if len(prediction) > 0 else 0
        else:
            pred_value = int(prediction)
        
        # Handle different probability formats
        if isinstance(probabilities, np.ndarray):
            if probabilities.ndim == 0:
                # Scalar ndarray
                prob_positive = float(probabilities)
            elif probabilities.size == 1:
                # Single element array
                prob_positive = float(probabilities.flat[0])
            elif probabilities.size == 2:
                # Two element array (negative and positive probabilities)
                prob_positive = float(probabilities[1])
            else:
                # Multiple samples or other shape, take first element
                prob_positive = float(probabilities.flat[0])
        elif isinstance(probabilities, (np.floating, float, int)):
            prob_positive = float(probabilities)
        elif isinstance(probabilities, (list, tuple)):
            prob_positive = float(probabilities[1]) if len(probabilities) > 1 else float(probabilities[0])
        else:
            prob_positive = float(probabilities)
        
        # Ensure probability is in [0, 1]
        prob_positive = max(0.0, min(1.0, prob_positive))
        prob_negative = 1.0 - prob_positive

        pred_label = "Positive" if pred_value == 1 else "Negative"

        response = {
            "prediction": pred_label,
            "confidence": round(prob_positive * 100, 2),
            "risk_level": risk_level,
            "probabilities": {
                "negative": round(prob_negative * 100, 2),
                "positive": round(prob_positive * 100, 2),
            },
        }

        if patient_id:
            response["patient_id"] = str(patient_id)

        return response

    @staticmethod
    def format_error_response(error_message: str, status_code: int = 400) -> Tuple[Dict[str, Any], int]:
        """
        Format error response.

        Args:
            error_message: Error description
            status_code: HTTP status code

        Returns:
            Tuple of (response dictionary, status code)
        """
        return {"error": error_message, "status": status_code}, status_code

    @staticmethod
    def format_history_response(records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Format prediction history response.

        Args:
            records: List of prediction records from database

        Returns:
            Formatted response
        """
        return {
            "total": len(records),
            "records": records,
            "status": "success",
        }
