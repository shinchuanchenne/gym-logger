from pwdlib import PasswordHash
from fastapi.security import OAuth2AuthorizationCodeBearer
from datetime import datetime, timedelta, timezone

password_hash = PasswordHash.recommended()

def hash_password(plain_password: str) -> str:
    return password_hash.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

