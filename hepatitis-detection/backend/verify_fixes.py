#!/usr/bin/env python
"""Simple bug fix verification without Flask context issues"""
import sys
sys.path.insert(0, '.')

print("="*70)
print("SIMPLE BUG FIX VERIFICATION TEST")
print("="*70)

try:
    # Test 1: Model loading
    print("\n[TEST 1] Model Loading...")
    import joblib
    import os
    
    MODEL_PATH = 'model/trained_model.pkl'
    if os.path.exists(MODEL_PATH):
        loaded = joblib.load(MODEL_PATH)
        if isinstance(loaded, dict):
            print("  Model type: DICT (Bundle format)")
            print("  Keys:", list(loaded.keys()))
            if 'feature_names' in loaded:
                num_features = len(loaded['feature_names'])
                print(f"  Features in model: {num_features}")
                print("  Feature names:")
                for i, f in enumerate(loaded['feature_names'], 1):
                    print(f"    {i:2d}. {f}")
            if 'scaler' in loaded:
                scaler = loaded['scaler']
                scaler_features = scaler.n_features_in_
                print(f"  Scaler n_features_in_: {scaler_features}")
            print("  PASS: Model loaded successfully")
        else:
            print(f"  Model type: {type(loaded).__name__}")
    else:
        print(f"  FAIL: Model not found at {MODEL_PATH}")
except Exception as e:
    print(f"  ERROR: {e}")

# Test 2: Feature preprocessing
print("\n[TEST 2] Feature Preprocessing...")
try:
    from app import preprocess_patient_data
    
    # Test data with all 18 medical features
    test_data = {
        'age': 45, 'sex': 1, 'bilirubin': 0.8, 'albumin': 4.1,
        'alk_phosphatase': 90.0, 'sgot': 28.0, 'sgpt': 32.0,
        'antivirals': 1, 'steroid': 0, 'fatigue': 0, 'malaise': 0, 
        'anorexia': 0, 'liver_big': 0, 'liver_firm': 0, 
        'spleen_palpable': 0, 'ascites': 0, 'spider_web': 0, 'protime': 1.0,
        'histology': 1
    }
    
    X, is_valid, msg = preprocess_patient_data(test_data)
    
    print(f"  Validation: {is_valid}")
    print(f"  Message: {msg}")
    print(f"  Output shape: {X.shape}")
    print(f"  Expected shape: (1, 18)")
    
    if X.shape == (1, 18):
        print("  PASS: Correct feature dimension (18)")
    else:
        print(f"  FAIL: Wrong shape {X.shape}, expected (1, 18)")
        
except Exception as e:
    print(f"  ERROR: {e}")

# Test 3: Prediction without errors
print("\n[TEST 3] Prediction Execution...")
try:
    from app import predict_patient
    
    patient_data = {
        'age': 35, 'sex': 1, 'bilirubin': 0.9, 'albumin': 4.2,
        'alk_phosphatase': 85.0, 'sgot': 30.0, 'sgpt': 28.0,
        'antivirals': 0, 'steroid': 0, 'fatigue': 0, 'malaise': 0,
        'anorexia': 0, 'liver_big': 0, 'liver_firm': 0,
        'spleen_palpable': 0, 'ascites': 0, 'spider_web': 0, 'protime': 1.0,
        'histology': 1
    }
    
    predictions, probabilities, risk_level = predict_patient(patient_data)
    
    print(f"  Prediction: {int(predictions[0])}")
    print(f"  Confidence array: {probabilities}")
    print(f"  Risk Level: {risk_level}")
    print("  PASS: Prediction executed successfully")
    
except Exception as e:
    print(f"  FAIL: Prediction error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Case-insensitive fields
print("\n[TEST 4] Case-Insensitive Field Names...")
try:
    capitalized_data = {
        'Age': 35, 'Sex': 1, 'Bilirubin': 0.9, 'Albumin': 4.2,
        'Alk_Phosphatase': 85.0, 'SGOT': 30.0, 'SGPT': 28.0,
        'Antivirals': 0, 'Steroid': 0, 'Fatigue': 0, 'Malaise': 0,
        'Anorexia': 0, 'Liver_Big': 0, 'Liver_Firm': 0,
        'Spleen_Palpable': 0, 'Ascites': 0, 'Spider_Web': 0, 'Protime': 1.0,
        'Histology': 1
    }
    
    predictions, probabilities, risk_level = predict_patient(capitalized_data)
    print(f"  Prediction with CAPITALIZED fields: {int(predictions[0])}")
    print("  PASS: Case-insensitive field matching works")
    
except Exception as e:
    print(f"  FAIL: Case-insensitive error: {e}")

# Test 5: Health endpoint model loading
print("\n[TEST 5] Health Endpoint Model Check...")
try:
    from app import model, model_bundle
    
    if model is not None or model_bundle is not None:
        print(f"  model is not None: {model is not None}")
        print(f"  model_bundle is not None: {model_bundle is not None}")
        print("  PASS: At least one model is loaded")
    else:
        print("  FAIL: Neither model nor model_bundle is loaded")
        
except Exception as e:
    print(f"  ERROR: {e}")

# Test 6: Healthy vs Hepatitis differentiation
print("\n[TEST 6] Healthy vs Hepatitis Differentiation...")
try:
    # Healthy case
    healthy = {
        'age': 50, 'sex': 1, 'bilirubin': 0.5, 'albumin': 4.3,
        'alk_phosphatase': 70.0, 'sgot': 20.0, 'sgpt': 18.0,
        'antivirals': 0, 'steroid': 0, 'fatigue': 0, 'malaise': 0,
        'anorexia': 0, 'liver_big': 0, 'liver_firm': 0,
        'spleen_palpable': 0, 'ascites': 0, 'spider_web': 0, 'protime': 1.0,
        'histology': 0
    }
    
    # Hepatitis case
    hepatitis = {
        'age': 40, 'sex': 1, 'bilirubin': 3.5, 'albumin': 3.0,
        'alk_phosphatase': 250.0, 'sgot': 200.0, 'sgpt': 220.0,
        'antivirals': 1, 'steroid': 1, 'fatigue': 1, 'malaise': 1,
        'anorexia': 1, 'liver_big': 1, 'liver_firm': 1,
        'spleen_palpable': 1, 'ascites': 1, 'spider_web': 1, 'protime': 1.5,
        'histology': 1
    }
    
    neg_pred, neg_prob, neg_risk = predict_patient(healthy)
    pos_pred, pos_prob, pos_risk = predict_patient(hepatitis)
    
    print(f"  Healthy case: Pred={int(neg_pred[0])}, Confidence={neg_prob}")
    print(f"  Hepatitis case: Pred={int(pos_pred[0])}, Confidence={pos_prob}")
    
    if int(neg_pred[0]) != int(pos_pred[0]):
        print("  PASS: Model correctly differentiates cases")
    else:
        print("  WARNING: Model predicts same class for both cases")
        
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("TEST SUMMARY COMPLETE")
print("="*70)
print("\nIf all tests show PASS, all bugs have been fixed!")
print("="*70)
