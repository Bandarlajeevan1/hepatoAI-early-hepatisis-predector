# Hepatitis Detection - Quick Start Guide

## Prerequisites

- Docker & Docker Compose (for containerized setup)
- OR: Python 3.11+, Node.js 18+, MongoDB 4.0+

## Quick Start with Docker

```bash
cd hepatitis-detection
docker compose up -d
```

Access the application at: **http://localhost:3000**

**Login Credentials (Create your own):**
- Register a new account on the login page
- System will provide authentication token

## Quick Start (Local Development)

### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start MongoDB (ensure it's running)
# mongod --dbpath C:\data\db

# Run Flask app
python app.py
```

Backend will be available at: **http://localhost:5000**

### 2. Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Start React development server
npm start
```

Frontend will open at: **http://localhost:3000**

## Available Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login

### Predictions
- `POST /predict` - Get hepatitis prediction
- `POST /save` - Save prediction to database
- `GET /history` - View prediction history

### System
- `GET /health` - Health check
- `GET /info` - API information
- `GET /apidocs` - Swagger documentation

## Test the System

```bash
# Run backend tests
cd backend
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Sample Prediction Request

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "sex": 1,
    "bilirubin": 0.8,
    "sgot": 25,
    "sgpt": 22,
    "albumin": 3.5,
    "protime": 12,
    "alk_phosphatase": 80,
    "malaise": 0,
    "anorexia": 0
  }'
```

## Environment Variables

Create `.env` file in `backend/` for local development:

```env
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
MONGO_URI=mongodb://localhost:27017/hepatitis_db
JWT_SECRET=your-secret-key-here
LOG_LEVEL=DEBUG
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MongoDB connection error | Ensure MongoDB is running or update MONGO_URI |
| Port 5000/3000 already in use | Change port in config.py and docker-compose.yml |
| Missing dependencies | Run `pip install -r requirements.txt` |
| Node modules error | Run `npm install` in frontend directory |

## Project Structure

```
hepatitis-detection/
├── backend/           # Flask REST API
│   ├── app.py        # Main application
│   ├── model/        # ML models
│   ├── database/     # MongoDB integration
│   └── tests/        # Unit tests
├── frontend/          # React UI
│   ├── src/          # React components
│   └── public/       # Static files
└── docker-compose.yml # Container orchestration
```

## Important Notes

- **Medical Disclaimer**: This application is for research/clinical support only
- **Not a substitute** for professional medical diagnosis
- **Always consult** qualified healthcare professionals
- **Model Performance**: Test with your own data before production use

## Support & Documentation

- See `README.md` for full documentation
- See `SETUP_AND_VERIFICATION.md` for detailed setup
- API docs available at `http://localhost:5000/apidocs`

---

**Version:** 1.0.0  
**Last Updated:** February 2026
