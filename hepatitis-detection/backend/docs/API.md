# Hepatitis Detection API Documentation

## Overview

The Hepatitis Detection API provides REST endpoints for predicting hepatitis status using a hybrid machine learning ensemble (MSEM) with FL-KNN and HDPSO components.

- **Base URL**: `http://localhost:5000`
- **API Version**: 1.0.0
- **Content-Type**: `application/json`

## Features

- **MSEM Ensemble**: Combines Random Forest, SVM, Logistic Regression, and XGBoost
- **FL-KNN Imputation**: Handles missing values intelligently
- **HDPSO Feature Selection**: Optimizes feature set for predictions
- **Database Integration**: Stores predictions in MongoDB
- **Input Validation**: Comprehensive patient data validation
- **OpenAPI/Swagger**: Interactive API documentation at `/apidocs`

---

## Endpoints

### 1. POST /predict

Predict hepatitis status for a patient based on medical features.

**Request**

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "sex": 1,
    "steroid": 1,
    "antivirals": 1,
    "fatigue": 1,
    "malaise": 1,
    "anorexia": 1,
    "liver_big": 1,
    "liver_firm": 1,
    "spleen_palpable": 0,
    "spider_web": 0,
    "ascites": 0,
    "varices": 0,
    "bilirubin": 0.8,
    "alk_phosphatase": 66,
    "sgot": 28,
    "sgpt": 25,
    "albumin": 4.0,
    "protime": 20
  }'
```

**Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| age | number | Yes | Age in years (0-120) |
| sex | integer | Yes | 1=Male, 2=Female |
| steroid | integer | No | Steroid usage (0/1/2) |
| antivirals | integer | No | Antiviral treatment (0/1/2) |
| fatigue | integer | No | Fatigue symptom (0/1/2) |
| malaise | integer | No | Malaise present (0/1) |
| anorexia | integer | No | Loss of appetite (0/1) |
| liver_big | integer | No | Enlarged liver (0/1) |
| liver_firm | integer | No | Liver firmness (0/1) |
| spleen_palpable | integer | No | Palpable spleen (0/1) |
| spider_web | integer | No | Spider web veins (0/1) |
| ascites | integer | No | Fluid in abdomen (0/1) |
| varices | integer | No | Esophageal varices (0/1) |
| bilirubin | number | No | Total bilirubin (mg/dL) |
| alk_phosphatase | number | No | Alkaline phosphatase (U/L) |
| sgot | number | No | SGOT/AST level (U/L) |
| sgpt | number | No | SGPT/ALT level (U/L) |
| albumin | number | No | Serum albumin (g/dL) |
| protime | number | No | Prothrombin time (seconds) |

**Response (Success - 200)**

```json
{
  "prediction": "Negative",
  "confidence": 78.50,
  "risk_level": "Low",
  "probabilities": {
    "negative": 78.50,
    "positive": 21.50
  }
}
```

**Response (Error - 400)**

```json
{
  "error": "Invalid input data. Check field values and types.",
  "status": 400
}
```

**Response (Error - 500)**

```json
{
  "error": "ML model not loaded. Please train the model first.",
  "status": 500
}
```

---

### 2. POST /save

Save a prediction result to the database.

**Request**

```bash
curl -X POST http://localhost:5000/save \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P123456",
    "prediction": "Negative",
    "confidence": 78.50,
    "risk_level": "Low",
    "input_data": {
      "age": 35,
      "sex": 1
    }
  }'
```

**Parameters**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| patient_id | string | No | Unique patient identifier |
| prediction | string | Yes | "Positive" or "Negative" |
| confidence | number | Yes | Confidence percentage (0-100) |
| risk_level | string | Yes | "Low", "Medium", or "High" |
| input_data | object | No | Patient medical data submitted |

**Response (Success - 200)**

```json
{
  "status": "success",
  "message": "Prediction saved successfully",
  "record_id": "507f1f77bcf86cd799439011",
  "timestamp": "2024-02-10T14:35:22.123456"
}
```

**Response (Error - 500)**

```json
{
  "error": "Failed to save: MongoDB connection failed",
  "status": 500
}
```

---

### 3. GET /history

Retrieve prediction history from the database.

**Request**

```bash
# Get last 50 predictions
curl -X GET "http://localhost:5000/history?limit=50" \
  -H "Content-Type: application/json"
```

**Query Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | integer | 100 | Maximum records to return (1-1000) |

**Response (Success - 200)**

```json
{
  "total": 25,
  "records": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "patient_id": "P123456",
      "prediction": "Negative",
      "confidence": 78.50,
      "risk_level": "Low",
      "timestamp": "2024-02-10T14:35:22.123456"
    },
    {
      "_id": "507f1f77bcf86cd799439012",
      "patient_id": "P123457",
      "prediction": "Positive",
      "confidence": 85.30,
      "risk_level": "High",
      "timestamp": "2024-02-10T14:30:15.654321"
    }
  ],
  "status": "success"
}
```

**Response (Error - 500)**

```json
{
  "error": "Failed to retrieve history: Database connection error",
  "status": 500
}
```

---

### 4. GET /health

Health check endpoint to verify API status.

**Request**

```bash
curl -X GET http://localhost:5000/health
```

**Response (Success - 200)**

```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-02-10T14:35:22.123456",
  "version": "1.0.0"
}
```

---

### 5. GET /info

Get API information and configuration.

**Request**

```bash
curl -X GET http://localhost:5000/info
```

**Response (Success - 200)**

```json
{
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
    "low": 0.3,
    "medium": 0.7
  }
}
```

---

## Risk Level Classification

Predictions are classified into risk levels based on the positive probability:

| Risk Level | Probability Range | Description |
|------------|------------------|-------------|
| **Low** | 0.0 - 0.3 | Low risk of hepatitis |
| **Medium** | 0.3 - 0.7 | Moderate risk, further testing recommended |
| **High** | 0.7 - 1.0 | High risk, immediate medical attention needed |

---

## Error Codes

| Status | Error | Meaning |
|--------|-------|---------|
| 400 | Invalid JSON content | Request body is not valid JSON |
| 400 | Invalid input data | Patient data fails validation |
| 400 | Missing required fields | Required fields are absent |
| 404 | Endpoint not found | API endpoint does not exist |
| 500 | Model not loaded | ML model not initialized |
| 500 | Database error | MongoDB connection or operation failed |
| 500 | Internal server error | Unexpected server error |

---

## Example Workflow

### Step 1: Make a Prediction

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "sex": 1,
    "bilirubin": 1.2,
    "sgot": 35,
    "sgpt": 40,
    "albumin": 3.8,
    "protime": 18
  }'
```

### Step 2: Save the Result

```bash
curl -X POST http://localhost:5000/save \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P789",
    "prediction": "Positive",
    "confidence": 82.5,
    "risk_level": "High"
  }'
```

### Step 3: View History

```bash
curl -X GET http://localhost:5000/history?limit=10
```

---

## Interactive API Documentation

Visit the interactive API documentation at:

- **Swagger UI**: `http://localhost:5000/apidocs`
- **ReDoc**: `http://localhost:5000/redoc`

The Swagger interface allows you to:
- Test all endpoints
- View request/response schemas
- Generate client code
- Explore detailed parameter descriptions

---

## Rate Limiting

Currently, no rate limiting is enforced. For production deployments, consider implementing:
- Request rate limiting (requests per minute)
- User authentication and API keys
- Request size limits

---

## Best Practices

1. **Always provide required fields** (age and sex)
2. **Validate input ranges** before submitting
3. **Handle network errors** with exponential backoff retries
4. **Cache predictions** to reduce API calls
5. **Log all predictions** for audit trails
6. **Use HTTPS in production** for secure data transmission

---

## Troubleshooting

### Model Not Loaded Error
**Cause**: The ML model file is missing or not trained
**Solution**: Run `python backend/train.py` to train the model

### MongoDB Connection Error
**Cause**: MongoDB service is not running or MONGO_URI is incorrect
**Solution**: 
- Start MongoDB service
- Check `MONGO_URI` in `.env` file
- Ensure MongoDB is accessible at the specified URI

### Invalid Input Data Error
**Cause**: Patient data fields are out of expected range or missing
**Solution**:
- Check field types (numbers vs. strings)
- Ensure age is between 0-120
- Verify categorical fields use valid values (0, 1, 2, "yes", "no")

### CORS Errors in Frontend
**Cause**: Cross-Origin Resource Sharing not properly configured
**Solution**: Flask-CORS is already enabled in app.py for all origins

---

## API Versioning

Current version: **1.0.0**

Future versions will maintain backward compatibility through:
- Deprecation warnings before breaking changes
- Separate endpoints for major version changes (`/v2/predict`)
- Extended response fields that are ignored by older clients

---

## Contact & Support

For issues, questions, or contributions:
- Visit: [Project Repository]
- Report bugs via GitHub Issues
- Submit feature requests

---

**Last Updated**: February 10, 2026  
**Status**: Production Ready
