from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from config.jwt_config import jwt_config
from logger.logger import error, warn
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify JWT token and extract user information"""
    token = credentials.credentials
    
    try:
        # Get the public key
        public_key = jwt_config.get_public_key()
        
        # Convert to PEM format for jose (python-jose expects PEM string)
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        
        # Verify and decode token
        payload = jwt.decode(
            token,
            public_key_pem,
            algorithms=["RS256"],
            options={"verify_signature": True, "verify_exp": True}
        )
        
        # Verify issuer
        issuer = payload.get("iss")
        if issuer != "ingesis.uniquindio.edu.co":
            warn("[JWT Middleware]", "Issuer inválido", {"issuer": issuer})
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token issuer inválido"
            )
        
        # Extract user_id from claims
        user_id = payload.get("userId")
        if not user_id:
            warn("[JWT Middleware]", "Token sin userId", {})
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token inválido: falta userId"
            )
        
        return {
            "user_id": user_id,
            "email": payload.get("sub"),
            "claims": payload
        }
        
    except JWTError as e:
        error("[JWT Middleware]", "Error validando token", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        error("[JWT Middleware]", "Error inesperado validando token", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno validando token"
        )

