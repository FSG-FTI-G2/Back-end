import os
import bcrypt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user import UserSchema
from dotenv import load_dotenv
from app.providers.jwt_provide import JWTProvider  # Import JWTProvider

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
jwt_provider = JWTProvider()  # Initialize JWTProvider

# Hash password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Create a new token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt_provider.encrypt(to_encode)  # Use JWTProvider to create token

# Verify login
async def authenticate_user(username: str, password: str):
    user = UserSchema.find_by_username(username)
    if not user or not verify_password(password, user.password):
        return None
    return user

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Unable to verify information",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt_provider.decrypt(token)  # Use JWTProvider to decrypt token
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = UserSchema.find_by_username(username)
    if user is None:
        raise credentials_exception
    return {"username": user.username, "id": user.id} 

