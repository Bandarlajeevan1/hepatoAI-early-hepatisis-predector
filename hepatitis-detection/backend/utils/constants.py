"""
Application constants for the Hepatitis Detection system.
"""

# ============================================================================
# CLASS LABELS
# ============================================================================
NEGATIVE_CLASS = "Negative"
POSITIVE_CLASS = "Positive"
CLASS_LABELS = [NEGATIVE_CLASS, POSITIVE_CLASS]

# ============================================================================
# RISK LEVELS
# ============================================================================
RISK_LOW = "Low"
RISK_MEDIUM = "Medium"
RISK_HIGH = "High"

# ============================================================================
# HEPATITIS DATASET FEATURES
# ============================================================================
# Common features in both Hepatitis and ILPD datasets
HEPATITIS_FEATURES = [
    "age",
    "sex",
    "steroid",
    "antivirals",
    "fatigue",
    "malaise",
    "anorexia",
    "liver_big",
    "liver_firm",
    "spleen_palpable",
    "spider_web",
    "ascites",
    "varices",
    "bilirubin",
    "alk_phosphatase",
    "sgot",
    "sgpt",
    "albumin",
    "protime",
    "histology",
]

ILPD_FEATURES = [
    "age",
    "sex",
    "aspartate_aminotransferase",
    "alamine_aminotransferase",
    "aspartate_aminotransferase_to_platelet_ratio",
    "total_bilirubin",
    "direct_bilirubin",
    "indirect_bilirubin",
    "alkaline_phosphatase",
    "total_protiens",
    "albumin",
    "albumin_to_globulin_ratio",
]

# ============================================================================
# CATEGORICAL FEATURES (for encoding)
# ============================================================================
CATEGORICAL_FEATURES = ["sex", "steroid", "antivirals", "fatigue"]
BINARY_FEATURES = [
    "malaise",
    "anorexia",
    "liver_big",
    "liver_firm",
    "spleen_palpable",
    "spider_web",
    "ascites",
    "varices",
    "histology",
]

# ============================================================================
# FEATURE RANGES & VALIDATION
# ============================================================================
# Typical ranges for validation (age, lab values, etc.)
FEATURE_RANGES = {
    "age": (0, 120),  # Age in years
    "bilirubin": (0, 20),  # mg/dL
    "alk_phosphatase": (0, 1000),  # U/L
    "sgot": (0, 1000),  # U/L (AST)
    "sgpt": (0, 1000),  # U/L (ALT)
    "albumin": (0, 100),  # g/dL or raw values
    "protime": (0, 100),  # seconds or raw values
}

# ============================================================================
# API RESPONSE MESSAGES
# ============================================================================
ERROR_MISSING_MODEL = "ML model not loaded. Please train the model first."
ERROR_MISSING_FIELDS = "Missing required patient data fields."
ERROR_INVALID_INPUT = "Invalid input data. Check field values and types."
ERROR_MONGODB_CONNECTION = "Database connection failed. Check MongoDB status."
ERROR_PREDICTION_FAILED = "Prediction failed. Please check input data."

SUCCESS_PREDICTION_SAVED = "Prediction saved successfully."
SUCCESS_HISTORY_RETRIEVED = "History retrieved successfully."

# ============================================================================
# DATABASE
# ============================================================================
PREDICTIONS_COLLECTION = "predictions"
PATIENTS_COLLECTION = "patients"
