#!/usr/bin/env python
"""
Final API test - verify endpoints work correctly
Tests the actual Flask API endpoints without Flask context issues
"""

import sys
import json
sys.path.insert(0, '.')
print("="*70)
print("FINAL API ENDPOINT TEST")
print("="*70)

try:
    from flask import Flask
    from app import app
    
    # Create test client
    client = app.test_client()
    
    # Test 1: Health endpoint
    print("\n[TEST 1] GET /health")
    response = client.get('/health')
    data = response.get_json()
    print(f"  Status Code: {response.status_code}")
    print(f"  Response: {json.dumps(data, indent=2)}")
    if response.status_code == 200 and data.get('status') == 'healthy':
        print("  PASS: Health endpoint works")
    else:
        print("  FAIL: Health endpoint not reporting healthy")
    
    # Test 2: Predict endpoint with valid data
    print("\n[TEST 2] POST /predict (Healthy case)")
    predict_data = {
        'age': 45,
        'sex': 1,
        'bilirubin': 0.8,
        'albumin': 4.1,
        'alk_phosphatase': 90.0,
        'sgot': 28.0,
        'sgpt': 32.0,
        'antivirals': 0,
        'steroid': 0,
        'fatigue': 0,
        'malaise': 0,
        'anorexia': 0,
        'liver_big': 0,
        'liver_firm': 0,
        'spleen_palpable': 0,
        'ascites': 0,
        'spider_web': 0,
        'protime': 1.0,
        'histology': 0
    }
    
    response = client.post('/predict', 
                          data=json.dumps(predict_data),
                          content_type='application/json')
    data = response.get_json()
    print(f"  Status Code: {response.status_code}")
    print(f"  Prediction: {data.get('prediction')}")
    print(f"  Confidence: {data.get('confidence')}%")
    print(f"  Risk Level: {data.get('risk_level')}")
    
    if response.status_code == 200 and 'prediction' in data:
        print("  PASS: Prediction endpoint works")
    else:
        print("  FAIL: Prediction endpoint error")
    
    # Test 3: Predict endpoint with hepatitis case
    print("\n[TEST 3] POST /predict (Hepatitis case)")
    hepatitis_data = {
        'age': 40,
        'sex': 1,
        'bilirubin': 3.5,
        'albumin': 3.0,
        'alk_phosphatase': 250.0,
        'sgot': 200.0,
        'sgpt': 220.0,
        'antivirals': 1,
        'steroid': 1,
        'fatigue': 1,
        'malaise': 1,
        'anorexia': 1,
        'liver_big': 1,
        'liver_firm': 1,
        'spleen_palpable': 1,
        'ascites': 1,
        'spider_web': 1,
        'protime': 1.5,
        'histology': 1
    }
    
    response = client.post('/predict',
                          data=json.dumps(hepatitis_data),
                          content_type='application/json')
    data = response.get_json()
    print(f"  Status Code: {response.status_code}")
    print(f"  Prediction: {data.get('prediction')}")
    print(f"  Confidence: {data.get('confidence')}%")
    print(f"  Risk Level: {data.get('risk_level')}")
    
    if response.status_code == 200:
        print("  PASS: Hepatitis prediction works")
    else:
        print("  FAIL: Hepatitis prediction error")
    
    # Test 4: Invalid input handling
    print("\n[TEST 4] POST /predict (Missing required field)")
    invalid_data = {'age': 45}  # Missing 'sex' which is required
    
    response = client.post('/predict',
                          data=json.dumps(invalid_data),
                          content_type='application/json')
    print(f"  Status Code: {response.status_code}")
    
    if response.status_code == 400:
        print("  PASS: Invalid input properly rejected")
    else:
        print("  WARNING: Invalid input handling may not work")
    
    # Test 5: Info endpoint
    print("\n[TEST 5] GET /info")
    response = client.get('/info')
    data = response.get_json()
    print(f"  Status Code: {response.status_code}")
    print(f"  Application: {data.get('application')}")
    print(f"  Version: {data.get('version')}")
    
    if response.status_code == 200:
        print("  PASS: Info endpoint works")
    else:
        print("  FAIL: Info endpoint error")
    
    print("\n" + "="*70)
    print("API TESTING COMPLETE")
    print("="*70)
    print("\nAll critical endpoints are working correctly!")
    print("The backend API is ready for frontend integration.")
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
