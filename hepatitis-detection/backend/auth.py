"""
Authentication module for user login and registration.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import os
from functools import wraps
from flask import request, jsonify, current_app
from bson.objectid import ObjectId

from database.mongo import db
from utils.logger import setup_logger

logger = setup_logger(__name__)

# JWT configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_EXPIRATION_HOURS = 24


class AuthService:
    """Service for handling user authentication."""

    @staticmethod
    def register(email: str, password: str, full_name: str = None) -> dict:
        """
        Register a new user.
        
        Args:
            email: User email
            password: User password
            full_name: User's full name (optional)
        
        Returns:
            Dictionary with success status and message
        """
        try:
            # Validate email format
            if not email or '@' not in email:
                return {'success': False, 'message': 'Invalid email format'}
            
            # Validate password length
            if not password or len(password) < 6:
                return {'success': False, 'message': 'Password must be at least 6 characters'}
            
            # Check if database is available
            if db is None:
                return {'success': False, 'message': 'Database connection failed. Please check MongoDB status.'}
            
            # Check if user already exists
            users_collection = db['users']
            existing_user = users_collection.find_one({'email': email.lower()})
            
            if existing_user:
                return {'success': False, 'message': 'Email already registered'}
            
            # Hash password
            hashed_password = generate_password_hash(password)
            
            # Create user document
            user_doc = {
                'email': email.lower(),
                'password': hashed_password,
                'full_name': full_name or email.split('@')[0],
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'is_active': True
            }
            
            # Insert user
            result = users_collection.insert_one(user_doc)
            
            logger.info(f"User registered successfully: {email}")
            return {
                'success': True,
                'message': 'Registration successful',
                'user_id': str(result.inserted_id)
            }
        
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return {'success': False, 'message': f'Registration failed: {str(e)}'}

    @staticmethod
    def login(email: str, password: str) -> dict:
        """
        Authenticate user and generate JWT token.
        
        Args:
            email: User email
            password: User password
        
        Returns:
            Dictionary with success status, token, and user info
        """
        try:
            # Validate inputs
            if not email or not password:
                return {'success': False, 'message': 'Email and password required'}
            
            # Check if database is available
            if db is None:
                return {'success': False, 'message': 'Database connection failed. Please check MongoDB status.'}
            
            # Find user
            users_collection = db['users']
            user = users_collection.find_one({'email': email.lower()})
            
            if not user:
                return {'success': False, 'message': 'Invalid email or password'}
            
            # Check if user is active
            if not user.get('is_active', False):
                return {'success': False, 'message': 'Account is inactive'}
            
            # Verify password
            if not check_password_hash(user['password'], password):
                return {'success': False, 'message': 'Invalid email or password'}
            
            # Generate JWT token
            token_payload = {
                'user_id': str(user['_id']),
                'email': user['email'],
                'full_name': user.get('full_name', ''),
                'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
            }
            
            token = jwt.encode(token_payload, JWT_SECRET, algorithm='HS256')
            
            logger.info(f"User logged in: {email}")
            return {
                'success': True,
                'message': 'Login successful',
                'token': token,
                'user': {
                    'user_id': str(user['_id']),
                    'email': user['email'],
                    'full_name': user.get('full_name', '')
                }
            }
        
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return {'success': False, 'message': f'Login failed: {str(e)}'}

    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verify JWT token.
        
        Args:
            token: JWT token
        
        Returns:
            Dictionary with success status and decoded payload
        """
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            return {'success': True, 'payload': payload}
        except jwt.ExpiredSignatureError:
            return {'success': False, 'message': 'Token has expired'}
        except jwt.InvalidTokenError:
            return {'success': False, 'message': 'Invalid token'}
        except Exception as e:
            return {'success': False, 'message': f'Token verification failed: {str(e)}'}


def token_required(f):
    """
    Decorator to protect routes with JWT authentication.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'success': False, 'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
        # Verify token
        result = AuthService.verify_token(token)
        if not result['success']:
            return jsonify(result), 401
        
        # Add decoded token to request context
        request.user = result['payload']
        return f(*args, **kwargs)
    
    return decorated
