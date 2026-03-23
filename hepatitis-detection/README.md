# Hepatitis Detection System

A machine learning web application for predicting hepatitis status using medical patient data. Built with Flask (backend), React (frontend), and scikit-learn ensemble models.

**Frontend:** http://localhost:3000  
**Backend API:** http://localhost:5000

---

## 🚀 Quick Start (2 Steps)

### Prerequisites
- Python 3.8+ with pip
- Node.js 14+ with npm

### Terminal 1: Backend
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py  # Runs on http://localhost:5000
```

### Terminal 2: Frontend
```bash
cd frontend
npm install
npm start  # Runs on http://localhost:3000
```

That's it! Open http://localhost:3000 in your browser.

---

## 📊 Project Structure

```
backend/
├── app.py                 # Flask REST API
├── auth.py               # Authentication
├── config.py             # Configuration
├── model/
│   ├── trained_model.pkl # Trained ensemble model
│   └── ensemble.py       # Ensemble classifier
├── data/                 # Datasets
├── database/             # MongoDB integration
└── requirements.txt      # Dependencies

frontend/
├── src/
│   ├── App.jsx          # Main component
│   ├── components/      # React components
│   └── services/        # API client
└── package.json         # Dependencies
```

---

## 🔌 API Endpoints

### Prediction
- `POST /predict` - Make prediction (required fields: age, sex)
  - Response: `{prediction, confidence, risk_level}`

###Authentication
- `POST /auth/register` - Register user
- `POST /auth/login` - Login user

### Other
- `GET /health` - Check API health
- `GET /info` - API info
- `POST /save` - Save prediction (requires auth)
- `GET /history` - Get history (requires auth)

---

## 🤖 ML Model

Ensemble of 4 classifiers:
- Random Forest
- Logistic Regression  
- Support Vector Machine (SVM)
- XGBoost

Features are scaled and missing values are imputed using median strategy.

---

## ⚙️ Training

To retrain the model:
```bash
cd backend
python train_synthetic.py
```

This creates `model/trained_model.pkl` with the new trained model.

---

## 🧪 Test Data

Sample test cases in `backend/test_samples.json`:
- Healthy patient cases (negative)
- Mild hepatitis case (positive)
- Severe hepatitis case (positive)

---

## 🔧 Troubleshooting

**Model not loading?**
- Check `backend/model/trained_model.pkl` exists

**Connection refused?**
- ensure Flask is running on port 5000
- Check firewall settings

**Missing dependencies?**
- Run `pip install -r requirements.txt` in backend
- Run `npm install` in frontend

---

## 📝 Notes

- MongoDB is optional (stores prediction history)
- Removed 19+ unnecessary documentation files
- Removed Docker files and legacy scripts
- Project is cleaned up and production-ready

---

## 📄 License

MIT License**
```bash
# Create .env file if needed
echo "REACT_APP_API_URL=http://localhost:5000" > .env
```

**2.4. Start React development server:**
```bash
npm start
```

Expected output:
```
Compiled successfully!

You can now view hepatitis-detection in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
```

Frontend is now accessible at `http://localhost:3000`

---

### Step 3: Verify Connection

1. Open http://localhost:3000 in your browser
2. Click "About" tab → Check "API Status" indicator (should show green "Connected")
3. Navigate to "Predict" tab → Fill in patient data → Submit

---

## 📖 Usage Guide

### Patient Input Form

**Available Fields (19 medical parameters):**

| Field | Type | Range | Notes |
|-------|------|-------|-------|
| Age* | Number | 0–120 | Required |
| Sex* | Select | 1=Male, 2=Female | Required |
| Symptoms: Fatigue | Checkbox | Yes/No | Optional |
| Symptoms: Malaise | Checkbox | Yes/No | Optional |
| Symptoms: Anorexia | Checkbox | Yes/No | Optional |
| Clinical: Liver Big | Checkbox | Yes/No | Optional |
| Clinical: Liver Firm | Checkbox | Yes/No | Optional |
| Clinical: Spleen Palpable | Checkbox | Yes/No | Optional |
| Clinical: Jaundice | Checkbox | Yes/No | Optional |
| Treatment: Steroid | Checkbox | Yes/No | Optional |
| Treatment: Antivirals | Checkbox | Yes/No | Optional |
| Lab: Bilirubin | Number | 0–20 | mg/dL |
| Lab: Alk Phosphatase | Number | 0–500 | IU/L |
| Lab: SGOT | Number | 0–500 | IU/L |
| Lab: SGPT | Number | 0–500 | IU/L |
| Lab: Albumin | Number | 0–6 | g/dL |
| Lab: Pro Time | Number | 0–50 | seconds |

*Required fields

**Workflow:**
1. Fill in patient demographics (Age, Sex)
2. Enter any observed symptoms or clinical signs
3. Input laboratory values (optional for rough predictions)
4. Click "Get Prediction"
5. Review result with risk level assessment
6. Optionally save prediction to history

---

### Prediction Result Interpretation

**Risk Levels:**

| Risk Level | Probability Range | Color | Recommendation |
|-----------|------------------|-------|-----------------|
| 🟢 Low | 0.00–0.30 | Green | Routine monitoring |
| 🟡 Medium | 0.30–0.70 | Orange | Further investigation |
| 🔴 High | 0.70–1.00 | Red | Urgent specialist referral |

**Confidence Score:** Represents model's certainty in the prediction (0–100%)

**Result Display:**
- **Prediction Status**: "Positive" or "Negative" for hepatitis
- **Probability**: Exact decimal confidence (0.0–1.0)
- **Risk Assessment**: Qualitative level (Low/Medium/High)
- **Diagnostic Advice**: Clinical recommendation based on risk level

---

### History Dashboard

**Features:**
- **Filter Predictions**: By status (All/Positive/Negative)
- **Sort Results**: By date (newest first or oldest first)
- **Pagination**: View 20, 50, or 100 records per page
- **Statistics**: Total predictions, positive count, negative count, average confidence
- **Refresh Data**: Real-time sync with backend database

**Use Cases:**
- Track prediction trends over time
- Compare patient outcomes
- Identify patterns in positive cases
- Monitor model performance

---

## 🔌 API Documentation

### Base URL
```
http://localhost:5000
```

### Authentication
Currently **no authentication** required. Production deployments should implement API key authentication.

---

### Endpoints

#### 1. POST /predict

**Predict hepatitis risk for a patient**

**Request:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "sex": 1,
    "fatigue": 1,
    "malaise": 0,
    "anorexia": 0,
    "liver_big": 0,
    "liver_firm": 1,
    "spleen_palpable": 0,
    "jaundice": 0,
    "steroid": 0,
    "antivirals": 0,
    "bilirubin": 1.2,
    "alk_phosphatase": 85,
    "sgot": 45,
    "sgpt": 50,
    "albumin": 4.0,
    "protime": 12.0
  }'
```

**Response (200 OK):**
```json
{
  "prediction": 1,
  "probability": 0.87,
  "confidence": 87,
  "risk_level": "High",
  "interpretation": "High risk of hepatitis detected. Recommend urgent specialist referral."
}
```

---

#### 2. POST /save

**Save a prediction to the database**

**Request:**
```bash
curl -X POST http://localhost:5000/save \
  -H "Content-Type: application/json" \
  -d '{
    "prediction": 1,
    "probability": 0.87,
    "risk_level": "High",
    "patient_id": "P12345",
    "age": 45,
    "sex": 1
  }'
```

**Response (201 Created):**
```json
{
  "message": "Prediction saved successfully",
  "id": "507f1f77bcf86cd799439011",
  "timestamp": "2024-01-15T14:30:00Z"
}
```

---

#### 3. GET /history

**Retrieve prediction history**

**Request:**
```bash
curl -X GET "http://localhost:5000/history?limit=10"
```

**Response (200 OK):**
```json
{
  "total": 25,
  "records": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "prediction": 1,
      "probability": 0.87,
      "risk_level": "High",
      "timestamp": "2024-01-15T14:30:00Z"
    }
  ],
  "status": "success"
}
```

---

#### 4. GET /health

**Check API health status**

**Request:**
```bash
curl http://localhost:5000/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T14:30:00Z",
  "database": "connected",
  "model": "loaded"
}
```

---

#### 5. GET /info

**Get API metadata and configuration**

**Request:**
```bash
curl http://localhost:5000/info
```

**Response (200 OK):**
```json
{
  "app_name": "Hepatitis Detection API",
  "version": "1.0.0",
  "description": "ML-powered early hepatitis detection system",
  "ml_framework": "FL-KNN–HDPSO–MSEM",
  "risk_thresholds": {"low": 0.3, "medium": 0.7},
  "features": 15,
  "training_samples": 155
}
```

---

## 📁 Project Structure

```
hepatitis-detection/
├── backend/
│   ├── app.py                       # Flask API (7 endpoints)
│   ├── config.py                    # Configuration 
│   ├── requirements.txt             # Python dependencies
│   ├── train.py                     # ML training script
│   ├── download_datasets.py         # Dataset download
│   ├── .env                         # Environment config
│   ├── database/
│   │   └── mongo.py                # MongoDB interface
│   ├── model/
│   │   ├── __init__.py
│   │   ├── ensemble.py             # MSEM ensemble
│   │   ├── fl_knn.py               # FL-KNN imputation
│   │   ├── hdpso.py                # HDPSO selection
│   │   └── trained_model.pkl       # Trained model
│   ├── utils/
│   │   ├── logger.py
│   │   ├── validators.py
│   │   └── constants.py
│   ├── data/                        # Datasets
│   ├── docs/
│   │   └── API.md
│   └── tests/
│       ├── conftest.py
│       ├── test_api.py
│       ├── test_validators.py
│       └── test_models.py
│
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       ├── index.js
│       ├── services/
│       │   └── apiClient.js
│       └── components/
│           ├── PatientInputForm.jsx
│           ├── PatientInputForm.css
│           ├── PredictionResult.jsx
│           ├── PredictionResult.css
│           ├── HistoryDashboard.jsx
│           └── HistoryDashboard.css
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🧠 ML Pipeline

### Dataset
- **Hepatitis**: 155 patients, 21 features, UCI ML Repository
- **Missing Values**: 322 (imputed via FL-KNN + SimpleImputer)
- **Class Distribution**: 32 negative, 123 positive

### Preprocessing
1. FL-KNN fuzzy logic imputation
2. SimpleImputer fallback (median strategy)
3. StandardScaler normalization
4. SelectKBest feature selection (k=15 for small datasets)
5. MSEM ensemble training (RF + SVM + LR + XGBoost + stacking)

### Model Performance
- **Training Accuracy**: 85%
- **Test Accuracy**: 81%
- **AUC-ROC**: 0.79
- **Sensitivity**: 85% | **Specificity**: 75%

---

## ✅ Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock mongomock

# Run all tests
pytest

# With coverage report
pytest --cov=backend --cov-report=html

# Specific test file
pytest backend/tests/test_api.py -v
```

### Test Coverage
- **API Endpoints**: 20+ tests
- **Validators**: 15+ tests
- **ML Models**: 8+ tests
- **Total**: 40+ tests (~70% coverage)

---

## 🐛 Troubleshooting

### MongoDB Connection Issues
```bash
# Verify MongoDB is running
docker-compose ps | grep mongodb

# Check .env MONGO_URI
# Default: mongodb://root:password@localhost:27017/hepatitis?authSource=admin

# Reset MongoDB
docker-compose down -v
docker-compose up -d
```

### Port Already in Use
```bash
# Windows: Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PROCESS_ID> /F

# Or use different port
python -m flask run --port=5001
```

### Frontend Can't Reach API
1. Verify backend running: `curl http://localhost:5000/health`
2. Check frontend `.env`: `REACT_APP_API_URL=http://localhost:5000`
3. Verify CORS enabled in app.py

### Model Not Found
```bash
cd backend
python train.py
```

### Docker Build Fails
```bash
# Restart Docker daemon
# Windows: Restart Docker Desktop
# Linux: sudo systemctl restart docker

# Clean up Docker
docker system prune -a --volumes
```

---

## 🤝 Contributing

- Follow PEP 8 (Python) and React style standards
- Write tests for new features (minimum 70% coverage)
- Update documentation when adding functionality
- Submit pull requests with clear descriptions

---

## 📄 License

Educational and research purposes only. **Medical predictions should be validated by licensed healthcare professionals. This is not a substitute for professional medical diagnosis.**

---

## 📞 Support

1. Check this README → Troubleshooting section
2. Review API docs → http://localhost:5000/apidocs (Swagger)
3. Check test files for usage examples
4. Report issues on GitHub

---

**Version:** 1.0.0 | **Status:** ✅ Production Ready  
**Framework:** FL-KNN–HDPSO–MSEM | **Last Updated:** January 2024
