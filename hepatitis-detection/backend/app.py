"""
Flask REST API for Hepatitis Detection using MSEM Ensemble with FL-KNN and HDPSO.

Endpoints:
  POST /auth/register - Register a new user
  POST /auth/login - Login user
  POST /predict - Predict hepatitis status for a patient
  POST /save - Save a prediction result to database
  GET /history - Retrieve prediction history
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from datetime import datetime
import numpy as np
import pandas as pd

from config import config
from model.fl_knn import FLKNNImputer
from model.ensemble import MSEMEnsemble
from database import mongo
from auth import AuthService, token_required
from utils.logger import setup_logger
from utils.validators import PatientDataValidator, ResponseValidator
from utils.constants import RISK_LOW, RISK_MEDIUM, RISK_HIGH, ERROR_MISSING_MODEL

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Swagger/OpenAPI documentation
swagger = Swagger(app)

# Setup logging
logger = setup_logger(__name__)

# Model artifacts
MODEL_PATH = os.path.join(os.path.dirname(__file__), config.MODEL_PATH)
model = None
scaler = None

# Load model at startup
def load_model():
    """Load trained MSEM ensemble model."""
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = MSEMEnsemble.load(MODEL_PATH)
            logger.info(f"✓ Loaded trained model from {MODEL_PATH}")
            return True
        except Exception as e:
            logger.error(f"Failed loading model: {e}")
            return False
    else:
        logger.warning(f"Model not found at {MODEL_PATH}. Run 'python train.py' first.")
        return False


# Load model when app starts (before any requests)
load_model()


def get_risk_level(probability: float) -> str:
    """
    Classify risk level based on prediction probability.
    
    Args:
        probability: Predicted probability (0.0 to 1.0)
    
    Returns:
        Risk level: "Low", "Medium", or "High"
    """
    if probability < config.RISK_THRESHOLD_LOW:
        return RISK_LOW
    elif probability < config.RISK_THRESHOLD_MEDIUM:
        return RISK_MEDIUM
    else:
        return RISK_HIGH


def preprocess_patient_data(patient_data: dict) -> tuple:
    """
    Preprocess patient input data for model prediction.
    
    Args:
        patient_data: Dictionary of patient features
    
    Returns:
        Tuple of (X_numeric numpy array, is_valid bool, error message)
    """
    try:
        # Validate input
        is_valid, validation_msg = PatientDataValidator.validate_prediction_input(patient_data)
        if not is_valid:
            return None, False, validation_msg
        
        # Sanitize input
        sanitized_data = PatientDataValidator.sanitize_input(patient_data)
        
        # If model provides feature names and imputer, build full feature vector
        if model is not None and getattr(model, 'feature_names', None):
          feature_names = model.feature_names
          # Create a row with all feature names initialized to NaN
          row = {fn: np.nan for fn in feature_names}
          # Fill with provided values
          for k, v in sanitized_data.items():
            if k in row:
              row[k] = v

          df_full = pd.DataFrame([row])
          # Convert columns to numeric where possible
          df_full = df_full.apply(pd.to_numeric, errors='coerce')
          X_full = df_full.to_numpy()

          # Apply imputer if available
          if getattr(model, 'imputer', None) is not None:
            try:
              X_imputed = model.imputer.transform(X_full)
            except Exception:
              X_imputed = np.nan_to_num(X_full, nan=np.nanmedian(X_full, axis=0))
          else:
            X_imputed = np.nan_to_num(X_full, nan=np.nanmedian(X_full, axis=0))

          return X_imputed, True, "Preprocessing successful"

        # Fallback: Convert to DataFrame and use numeric columns provided by input
        df = pd.DataFrame([sanitized_data])
        # Extract numeric features
        X_numeric = df.select_dtypes(include=[np.number]).to_numpy()
        if X_numeric.shape[1] == 0:
          return None, False, "No numeric features found in input"
        # Handle NaN values with simple median imputation
        X_numeric = np.nan_to_num(X_numeric, nan=np.nanmedian(X_numeric))
        return X_numeric, True, "Preprocessing successful"
    
    except Exception as e:
        return None, False, f"Preprocessing error: {str(e)}"


def predict_patient(patient_data: dict) -> tuple:
    """
    Preprocess input dict and run model prediction returning prediction and probabilities.

    Returns:
        (predictions_array, probabilities_array, risk_level_str)
    """
    if model is None:
        raise RuntimeError(ERROR_MISSING_MODEL)

    X, is_valid, msg = preprocess_patient_data(patient_data)
    if not is_valid:
        raise ValueError(msg)

    # Ensure row shape
    if X.ndim == 1:
        X = X.reshape(1, -1)
    if X.shape[0] != 1:
        X = X.reshape(1, -1)

    # If selector expects a different number of input features, try to recover
    selector = getattr(model, 'selector', None)
    if selector is not None and hasattr(selector, 'n_features_in_'):
        expected = selector.n_features_in_
        if X.shape[1] != expected:
            # Attempt to re-run imputer (if available) on a full-feature row
            imp = getattr(model, 'imputer', None)
            if imp is not None:
                try:
                    # attempt to build a full row from feature_names if available
                    fn = getattr(model, 'feature_names', None)
                    if fn is not None and len(fn) == X.shape[1]:
                        X_full = X
                    else:
                        # pad or trim to match selector input
                        if X.shape[1] > expected:
                            X = X[:, :expected]
                        else:
                            # pad with medians
                            pad = np.nanmedian(X, axis=0)
                            pad = np.resize(pad, expected)
                            X = np.concatenate([X, pad.reshape(1, -1)[:, X.shape[1]:]], axis=1)
                except Exception:
                    pass

    # Run prediction
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)

    # Determine probability for positive class
    if getattr(probabilities, 'ndim', None) == 1:
        prob_positive = float(probabilities[0])
    elif probabilities.shape[1] > 1:
        prob_positive = float(probabilities[0, 1])
    else:
        prob_positive = float(probabilities[0, 0])

    risk_level = get_risk_level(prob_positive)

    return predictions, probabilities, risk_level


@app.route("/auth/register", methods=["POST"])
def register():
    """
    Register a new user.
    
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "user@example.com"
            password:
              type: string
              example: "password123"
            full_name:
              type: string
              example: "John Doe"
    responses:
      201:
        description: User registered successfully
      400:
        description: Registration failed
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Invalid JSON'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()
        
        result = AuthService.register(email, password, full_name)
        status_code = 201 if result['success'] else 400
        
        return jsonify(result), status_code
    
    except Exception as e:
        logger.error(f"Register error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error'}), 500


@app.route("/auth/login", methods=["POST"])
def login():
    """
    Login user and get JWT token.
    
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "user@example.com"
            password:
              type: string
              example: "password123"
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            token:
              type: string
            user:
              type: object
      400:
        description: Login failed
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Invalid JSON'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        result = AuthService.login(email, password)
        status_code = 200 if result['success'] else 401
        
        return jsonify(result), status_code
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error'}), 500


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict hepatitis status for a patient.
    
    ---
    tags:
      - Prediction
    parameters:
      - in: body
        name: body
        description: Patient medical data for prediction
        required: true
        schema:
          type: object
          required:
            - age
            - sex
          properties:
            age:
              type: number
              example: 35
            sex:
              type: integer
              description: "1 or 2 (male/female)"
              example: 1
            bilirubin:
              type: number
              example: 0.8
            sgot:
              type: number
              example: 25
            sgpt:
              type: number
              example: 22
    responses:
      200:
        description: Prediction successful
        schema:
          type: object
          properties:
            prediction:
              type: string
              enum: ["Positive", "Negative"]
            confidence:
              type: number
              description: "Confidence percentage (0-100)"
            risk_level:
              type: string
              enum: ["Low", "Medium", "High"]
            probabilities:
              type: object
              properties:
                negative:
                  type: number
                positive:
                  type: number
      400:
        description: Invalid input
      500:
        description: Server error or model not loaded
    """
    if model is None:
        logger.error("Model not loaded")
        return ResponseValidator.format_error_response(ERROR_MISSING_MODEL, 500)
    
    try:
        # Get JSON payload
        payload = request.get_json()
        if payload is None:
            return ResponseValidator.format_error_response("Invalid JSON content", 400)
        # Use helper to preprocess and predict
        try:
            predictions, probabilities, risk_level = predict_patient(payload)
        except ValueError as ve:
            logger.warning(f"Invalid input: {ve}")
            return ResponseValidator.format_error_response(str(ve), 400)

        response_data = ResponseValidator.format_prediction_response(
            predictions, probabilities[0], risk_level
        )

        logger.info(f"✓ Prediction: {response_data['prediction']} (confidence: {response_data['confidence']}%)")
        return jsonify(response_data), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return ResponseValidator.format_error_response(f"Prediction failed: {str(e)}", 500)


@app.route("/save", methods=["POST"])
def save():
    """
    Save a prediction result to MongoDB.
    
    ---
    tags:
      - Database
    parameters:
      - in: body
        name: body
        description: Prediction data to save
        required: true
        schema:
          type: object
          properties:
            patient_id:
              type: string
            prediction:
              type: string
            confidence:
              type: number
            risk_level:
              type: string
            input_data:
              type: object
    responses:
      200:
        description: Prediction saved successfully
      400:
        description: Invalid input
      500:
        description: Database error
    """
    try:
        payload = request.get_json()
        if payload is None:
            return ResponseValidator.format_error_response("Invalid JSON content", 400)
        
        # Add metadata
        record = payload.copy()
        record["timestamp"] = datetime.utcnow().isoformat()
        
        # Insert into MongoDB
        result_id = mongo.insert_prediction(record)
        logger.info(f"✓ Saved prediction to database: {result_id}")
        
        return jsonify({
            "status": "success",
            "message": "Prediction saved successfully",
            "record_id": str(result_id),
            "timestamp": record["timestamp"]
        }), 200
    
    except Exception as e:
        logger.error(f"Database save error: {str(e)}")
        return ResponseValidator.format_error_response(f"Failed to save: {str(e)}", 500)


@app.route("/history", methods=["GET"])
def history():
    """
    Retrieve prediction history from MongoDB.
    
    ---
    tags:
      - Database
    parameters:
      - in: query
        name: limit
        type: integer
        default: 100
        description: Maximum number of records to return
    responses:
      200:
        description: Successfully retrieved history
        schema:
          type: object
          properties:
            total:
              type: integer
            records:
              type: array
            status:
              type: string
      500:
        description: Database error
    """
    try:
        limit = request.args.get("limit", default=100, type=int)
        limit = min(limit, 1000)  # Cap at 1000 records
        
        records = mongo.get_history(limit=limit)
        logger.info(f"✓ Retrieved {len(records)} prediction records")
        
        response = ResponseValidator.format_history_response(records)
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        return ResponseValidator.format_error_response(f"Failed to retrieve history: {str(e)}", 500)


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    
    ---
    tags:
      - System
    responses:
      200:
        description: Service is healthy
    """
    status = {
        "status": "healthy" if model is not None else "degraded",
        "model_loaded": model is not None,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
    return jsonify(status), 200


@app.route("/info", methods=["GET"])
def info():
    """
    Get API information and configuration.
    
    ---
    tags:
      - System
    responses:
      200:
        description: API information
    """
    info_data = {
        "application": "Hepatitis Detection - MSEM Ensemble",
        "version": "1.0.0",
        "model": "MSEM with FL-KNN imputation and HDPSO feature selection",
        "endpoints": {
            "predict": "POST /predict",
            "save": "POST /save",
            "history": "GET /history",
            "health": "GET /health",
            "info": "GET /info"
        },
        "risk_thresholds": {
            "low": config.RISK_THRESHOLD_LOW,
            "medium": config.RISK_THRESHOLD_MEDIUM
        }
    }
    return jsonify(info_data), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return ResponseValidator.format_error_response("Endpoint not found", 404)


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return ResponseValidator.format_error_response("Internal server error", 500)


if __name__ == "__main__":
    # Load model before starting server
    load_model()
    
    logger.info("Starting Flask API server...")
    app.run(
        host="0.0.0.0",
        port=config.FLASK_PORT,
        debug=config.DEBUG,
        use_reloader=False  # Important when model is loaded at startup
    )