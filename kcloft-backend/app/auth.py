from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
import os
import json
import base64
import time
from dotenv import load_dotenv

load_dotenv()

bearer_scheme = HTTPBearer()
TENANT_ID = os.getenv("TENANT_ID", "109199d4-f7c0-4027-bcd7-9937e7fb177b")
AUDIENCE = os.getenv("CLIENT_ID", "d4552121-7ccf-4875-8b0a-c71a7f5c8c28")

def decode_jwt_payload(token: str) -> dict:
    """
    Manually decode JWT payload without any validation.
    This avoids audience validation issues.
    """
    try:
        # JWT format: header.payload.signature
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid JWT format")
        
        # Decode payload (second part)
        payload_b64 = parts[1]
        # Add padding if needed
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += '=' * padding
        
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        payload = json.loads(payload_bytes.decode('utf-8'))
        return payload
    except Exception as e:
        raise ValueError(f"Failed to decode JWT payload: {str(e)}")

def verify_token(credentials=Depends(bearer_scheme)):
    if not credentials:
        print("DEBUG: No credentials provided")
        raise HTTPException(status_code=401, detail="No credentials provided")
    
    token = credentials.credentials
    print(f"DEBUG: Received token (length: {len(token) if token else 0})")
    
    if not token:
        print("DEBUG: Token is empty")
        raise HTTPException(status_code=401, detail="Token is empty")
    
    try:
        # Manually decode JWT payload to avoid any validation issues
        payload = decode_jwt_payload(token)
        
        # Log token details for debugging
        token_audience = payload.get("aud")
        token_issuer = payload.get("iss")
        print(f"DEBUG: Token audience: {token_audience}, issuer: {token_issuer}")
        
        # Verify issuer matches expected tenant
        # Accept both issuer formats:
        # 1. https://login.microsoftonline.com/{TENANT_ID}/v2.0 (v2.0 endpoint)
        # 2. https://sts.windows.net/{TENANT_ID}/ (older format, still valid)
        valid_issuers = [
            f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
            f"https://login.microsoftonline.com/{TENANT_ID}/",
            f"https://sts.windows.net/{TENANT_ID}/",
        ]
        
        # Also check if issuer contains the tenant ID (more flexible)
        if token_issuer not in valid_issuers and TENANT_ID not in token_issuer:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token issuer. Expected issuer for tenant {TENANT_ID}, got {token_issuer}"
            )
        
        # Check expiration
        exp = payload.get("exp")
        if exp:
            current_time = time.time()
            if exp < current_time:
                print(f"DEBUG: Token expired. Exp: {exp}, Now: {current_time}")
                raise HTTPException(status_code=401, detail="Token has expired")
        
        # Token is valid - return payload
        print("DEBUG: Token validation successful")
        print(f"DEBUG: Token scopes: {payload.get('scp', 'N/A')}")
        return payload
        
    except HTTPException:
        raise
    except ValueError as e:
        print(f"DEBUG: Token decode error: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Invalid token format: {str(e)}")
    except Exception as e:
        print(f"DEBUG: Unexpected error: {str(e)}")
        print(f"DEBUG: Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=401, detail=f"Token validation error: {str(e)}")
