from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
import jwt

from typing import Annotated
from datetime import datetime, timedelta, timezone

from backend.models.employee import EmployeeUser

SECRET_KEY = 'aboba'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
_token = Annotated[str, Depends(_oauth2_scheme)]

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def _get_current_user(token: _token) -> EmployeeUser:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        data = decode_token(token)
    except jwt.InvalidTokenError:
        raise credentials_exception
    # if 'employee' not in data.get('scope')
    return EmployeeUser(
        uuid=data['employeeUUID'],
    )

get_current_user = Annotated[EmployeeUser, Depends(_get_current_user)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
