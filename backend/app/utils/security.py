import hashlib
import hmac
import os
from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.config import get_settings


def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
    return f"{salt}${password_hash}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt, saved_hash = password_hash.split("$", 1)
    except ValueError:
        return False
    new_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
    return hmac.compare_digest(new_hash, saved_hash)


def create_access_token(subject: str) -> str:
    settings = get_settings()
    expires_at = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> str | None:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload.get("sub")
    except JWTError:
        return None
