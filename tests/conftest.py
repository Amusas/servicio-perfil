# tests/conftest.py
import pytest
import os
import sys
from unittest.mock import MagicMock, patch, Mock
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from jose import jwt

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set test environment
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '5432'
os.environ['DB_USER'] = 'test_user'
os.environ['DB_PASSWORD'] = 'test_password'
os.environ['DB_NAME'] = 'test_db'
os.environ['PUBLIC_KEY_PATH'] = '/tmp/test_public_key.pem'

# CRITICAL: Mock database BEFORE any imports
sys.modules['psycopg2'] = MagicMock()
sys.modules['psycopg2.pool'] = MagicMock()

# Create dummy public key file for JWT config
dummy_key_path = '/tmp/test_public_key.pem'
if not os.path.exists(dummy_key_path):
    # Generate a test RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Write public key to temp file
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(dummy_key_path, 'wb') as f:
        f.write(public_pem)


@pytest.fixture
def rsa_keys():
    """Generate RSA key pair for testing"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    # Serialize keys
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    return {
        'private_key': private_key,
        'public_key': public_key,
        'private_pem': private_pem,
        'public_pem': public_pem
    }


@pytest.fixture
def valid_token(rsa_keys):
    """Generate a valid JWT token for testing"""
    payload = {
        "userId": 1,
        "sub": "test@example.com",
        "iss": "ingesis.uniquindio.edu.co",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        rsa_keys['private_pem'],
        algorithm='RS256'
    )

    return token


@pytest.fixture
def expired_token(rsa_keys):
    """Generate an expired JWT token for testing"""
    payload = {
        "userId": 1,
        "sub": "test@example.com",
        "iss": "ingesis.uniquindio.edu.co",
        "exp": datetime.utcnow() - timedelta(hours=1),
        "iat": datetime.utcnow() - timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        rsa_keys['private_pem'],
        algorithm='RS256'
    )

    return token


@pytest.fixture
def invalid_issuer_token(rsa_keys):
    """Generate a token with invalid issuer"""
    payload = {
        "userId": 1,
        "sub": "test@example.com",
        "iss": "invalid.issuer.com",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        rsa_keys['private_pem'],
        algorithm='RS256'
    )

    return token


@pytest.fixture
def mock_db_connection():
    """Mock database connection"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_cursor.fetchall.return_value = []

    return mock_conn, mock_cursor


@pytest.fixture
def sample_profile_data():
    """Sample profile data for testing"""
    return {
        "id": 1,
        "user_id": 1,
        "personal_url": "https://example.com",
        "nickname": "testuser",
        "is_contact_public": True,
        "mailing_address": "123 Test St",
        "biography": "Test bio",
        "organization": "Test Org",
        "country": "Colombia",
        "social_links": {"twitter": "https://twitter.com/test"},
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@pytest.fixture(autouse=True)
def mock_database_config():
    """Mock database configuration to avoid real connections"""
    # This fixture runs automatically for all tests
    pass  # Database is already mocked at module level