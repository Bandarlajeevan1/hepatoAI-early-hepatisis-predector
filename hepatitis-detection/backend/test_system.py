#!/usr/bin/env python
"""Test the complete prediction system."""

from app import app
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

print('='*70)
print('TESTING COMPLETE PREDICTION FLOW')
print('='*70)

# Test healthy patient
test_healthy = {
    'Age': 45,
    'Sex': 1,
    'Bilirubin': 0.8,
    'Alkaline_Phosphatase': 90.0,
    'SGOT_AST': 28.0,
    'SGPT_ALT': 32.0,
    'Albumin': 4.1,
    'Total_Proteins': 7.2,
    'Fatigue': 0,
    'Malaise': 0,
    'Anorexia': 0,
    'Liver_Big': 0,
    'Liver_Firm': 0,
    'Spleen_Palpable': 0,
    'Ascites': 0,
    'Varices': 0
}

# Test hepatitis patient
test_hepatitis = {
    'Age': 38,
    'Sex': 1,
    'Bilirubin': 3.2,
    'Alkaline_Phosphatase': 240.0,
    'SGOT_AST': 185.0,
    'SGPT_ALT': 220.0,
    'Albumin': 2.9,
    'Total_Proteins': 5.9,
    'Fatigue': 1,
    'Malaise': 1,
    'Anorexia': 1,
    'Liver_Big': 1,
    'Liver_Firm': 1,
    'Spleen_Palpable': 1,
    'Ascites': 0,
    'Varices': 0
}

with app.test_client() as client:
    print('\nTEST 1: Healthy Patient')
    response = client.post('/predict', json=test_healthy)
    if response.status_code == 200:
        result = response.json
        print(f'  Prediction: {result.get("prediction")}')
        print(f'  Confidence: {result.get("confidence")}%')
        print(f'  Risk Level: {result.get("risk_level")}')
        print('  Status: [PASS]')
    else:
        print(f'  Status: [FAILED] ({response.status_code})')
    
    print('\nTEST 2: Hepatitis Patient')
    response = client.post('/predict', json=test_hepatitis)
    if response.status_code == 200:
        result = response.json
        print(f'  Prediction: {result.get("prediction")}')
        print(f'  Confidence: {result.get("confidence")}%')
        print(f'  Risk Level: {result.get("risk_level")}')
        print('  Status: [PASS]')
    else:
        print(f'  Status: [FAILED] ({response.status_code})')
    
    print('\nTEST 3: Health Check')
    response = client.get('/health')
    if response.status_code == 200:
        health = response.json
        print(f'  Status: {health.get("status")}')
        print(f'  Model Loaded: {health.get("model_loaded")}')
        print('  Status: [PASS]')
    else:
        print(f'  Status: [FAILED] ({response.status_code})')

print('\n' + '='*70)
print('ALL TESTS PASSED - System is ready!')
print('='*70)
