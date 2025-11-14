import os
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class JWTConfig:
    def __init__(self):
        self.public_key_path = os.getenv("PUBLIC_KEY_PATH", "/app/keys/public-key.pem")
        self._public_key = None
        self._load_public_key()
    
    def _load_public_key(self):
        """Load RSA public key from PEM file"""
        try:
            with open(self.public_key_path, 'r') as f:
                pem_data = f.read()
            
            self._public_key = serialization.load_pem_public_key(
                pem_data.encode(),
                backend=default_backend()
            )
        except Exception as e:
            raise Exception(f"Error loading public key: {str(e)}")
    
    def get_public_key(self):
        """Get the public key for JWT verification"""
        return self._public_key


# Global JWT config instance
jwt_config = JWTConfig()

