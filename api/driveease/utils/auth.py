import base64
import hmac
import hashlib
import json
import time

def is_authorized(profile):
    """
    Centralized Authorization Logic
    profile should be a dict with at least 'email'.
    """
    email = (profile.get('email') or '').lower().strip()
    if not email:
        return False
        
    parts = email.split('@')
    if len(parts) != 2:
        return False
    domain = parts[1]

    public_whitelist = [
        'gmail.com',
        'yahoo.com',
        'outlook.com',
        'microsoft.com'
    ]

    return (
        domain in public_whitelist
    )

def base64url_encode(data):
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def create_jwt(payload, secret):
    """
    Generate a JWT token using HS256.
    Matches the Nuxt implementation.
    """
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = base64url_encode(json.dumps(header).encode('utf-8'))
    
    now = int(time.time())
    full_payload = {**payload, "iat": now, "exp": now + 60 * 60 * 5} # 5 hours
    payload_b64 = base64url_encode(json.dumps(full_payload).encode('utf-8'))
    
    signature = hmac.new(
        secret.encode('utf-8'),
        f"{header_b64}.{payload_b64}".encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    signature_b64 = base64url_encode(signature)
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def verify_jwt(token, secret):
    """
    Verify a JWT token and return the payload if valid.
    Raises ValueError if invalid.
    """
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid token format")
        
    header_b64, payload_b64, signature_b64 = parts
    
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        f"{header_b64}.{payload_b64}".encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    expected_signature_b64 = base64url_encode(expected_signature)
    
    if signature_b64 != expected_signature_b64:
        raise ValueError("Invalid signature")
        
    # Add padding back if necessary
    pad = len(payload_b64) % 4
    if pad > 0:
        payload_b64 += '=' * (4 - pad)
        
    try:
        payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode('utf-8'))
    except Exception:
        raise ValueError("Invalid payload")
        
    if payload.get('exp', 0) < int(time.time()):
        raise ValueError("Token expired")
        
    return payload