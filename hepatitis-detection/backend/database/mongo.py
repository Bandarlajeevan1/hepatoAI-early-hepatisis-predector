"""
MongoDB integration for storing patient records and predictions.
"""
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Use Atlas URI from environment or fall back to local Docker Mongo if not provided
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://jeevanbandarla1234_db_user:Jeevan12@cluster0.eg83ljt.mongodb.net/"
)


def get_client(timeout=5000):
    """
    Get MongoDB client with timeout.
    
    Args:
        timeout: Connection timeout in milliseconds
    
    Returns:
        MongoClient instance
    
    Raises:
        ConnectionFailure: If connection fails
    """
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=timeout)
        # Test connection
        client.admin.command('ping')
        logger.info("✓ Connected to MongoDB")
        return client
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise ConnectionFailure(f"MongoDB connection failed: {e}")


def get_db(name="hepatitis_db"):
    """Get database instance."""
    try:
        client = get_client()
        return client[name]
    except ConnectionFailure as e:
        logger.error(f"Database connection error: {e}")
        raise


def insert_prediction(record, db_name="hepatitis_db"):
    """
    Insert a prediction record into MongoDB.
    
    Args:
        record: Dictionary containing prediction data
        db_name: Database name
    
    Returns:
        Inserted document ID
    
    Raises:
        ConnectionFailure: If database connection fails
    """
    try:
        db = get_db(db_name)
        coll = db.get_collection("predictions")
        
        # Add timestamp if not present
        if "timestamp" not in record:
            record["timestamp"] = datetime.utcnow()
        
        # Insert document
        result = coll.insert_one(record)
        logger.info(f"✓ Inserted prediction record: {result.inserted_id}")
        return result.inserted_id
    
    except ConnectionFailure as e:
        logger.error(f"Failed to insert prediction: {e}")
        raise
    except Exception as e:
        logger.error(f"Database insert error: {e}")
        raise


def get_history(limit=100, db_name="hepatitis_db", filter_query=None):
    """
    Retrieve prediction history from MongoDB.
    
    Args:
        limit: Maximum number of records to return
        db_name: Database name
        filter_query: Optional MongoDB filter query
    
    Returns:
        List of prediction records
    
    Raises:
        ConnectionFailure: If database connection fails
    """
    try:
        db = get_db(db_name)
        coll = db.get_collection("predictions")
        
        # Create query
        query = filter_query or {}
        
        # Fetch documents, sorted by timestamp (newest first)
        documents = list(
            coll.find(query)
            .sort("timestamp", -1)
            .limit(limit)
        )
        
        # Convert ObjectId to string for JSON serialization
        for doc in documents:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            if "timestamp" in doc and hasattr(doc["timestamp"], "isoformat"):
                doc["timestamp"] = doc["timestamp"].isoformat()
        
        logger.info(f"✓ Retrieved {len(documents)} prediction records")
        return documents
    
    except ConnectionFailure as e:
        logger.error(f"Failed to retrieve history: {e}")
        raise
    except Exception as e:
        logger.error(f"Database query error: {e}")
        raise


def delete_old_records(days=30, db_name="hepatitis_db"):
    """
    Delete prediction records older than specified days.
    
    Args:
        days: Number of days to keep
        db_name: Database name
    
    Returns:
        Number of deleted records
    """
    try:
        from datetime import timedelta
        db = get_db(db_name)
        coll = db.get_collection("predictions")
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = coll.delete_many({"timestamp": {"$lt": cutoff_date}})
        
        logger.info(f"✓ Deleted {result.deleted_count} old records")
        return result.deleted_count
    
    except Exception as e:
        logger.error(f"Failed to delete old records: {e}")
        raise


def get_stats(db_name="hepatitis_db"):
    """
    Get prediction statistics.
    
    Args:
        db_name: Database name
    
    Returns:
        Dictionary with statistics
    """
    try:
        db = get_db(db_name)
        coll = db.get_collection("predictions")
        
        total_predictions = coll.count_documents({})
        positive_predictions = coll.count_documents({"prediction": "Positive"})
        negative_predictions = coll.count_documents({"prediction": "Negative"})
        
        stats = {
            "total_predictions": total_predictions,
            "positive_count": positive_predictions,
            "negative_count": negative_predictions,
            "positive_percentage": (positive_predictions / total_predictions * 100) if total_predictions > 0 else 0
        }
        
        return stats
    
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        return None

# Initialize database connection for module-level import
try:
    db = get_db()
except Exception as e:
    logger.warning(f"Could not initialize database on import: {e}")
    db = None