"""
Centralized configuration for the Hepatitis Detection application.
Loads from environment variables with sensible defaults.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration."""

    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/hepatitis_db")
    MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
    MONGODB_PORT = int(os.getenv("MONGODB_PORT", "27017"))
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "hepatitis_db")

    # Flask
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # Application
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MODEL_PATH = os.getenv("MODEL_PATH", "model/trained_model.pkl")

    # ML Pipeline
    N_NEIGHBORS_KNN = int(os.getenv("N_NEIGHBORS_KNN", "5"))
    RSEED = int(os.getenv("RSEED", "42"))

    # Risk Thresholds (probability-based)
    RISK_THRESHOLD_LOW = float(os.getenv("RISK_THRESHOLD_LOW", "0.3"))
    RISK_THRESHOLD_MEDIUM = float(os.getenv("RISK_THRESHOLD_MEDIUM", "0.7"))

    # Collections
    PREDICTIONS_COLLECTION = "predictions"
    PATIENTS_COLLECTION = "patients"


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    LOG_LEVEL = "INFO"
    MODEL_PATH = os.getenv("MODEL_PATH", "/app/model/trained_model.pkl")


class TestingConfig(Config):
    """Testing configuration."""

    MONGO_URI = os.getenv("TEST_MONGO_URI", "mongodb://localhost:27017/hepatitis_test_db")
    MONGODB_DATABASE = "hepatitis_test_db"
    DEBUG = True
    LOG_LEVEL = "DEBUG"


def get_config():
    """Get configuration based on Flask environment."""
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()


config = get_config()
