import os
import bcrypt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from app.models.user import UserSchema  
from dotenv import load_dotenv
from app.models.user import UserSchema
from datetime import timedelta

load_dotenv()

SECRET_KEY = os.environ.get("JWT_SECRET") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Hash password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Create a new token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#Create admin
def create_mock_admin():
    admin = UserSchema(
        username="admin",
        password=hash_password("admin1111"),  
        is_admin= True
    )
    admin.create()
    return admin

# Verify login
async def authenticate_user(username: str, password: str):
    user = UserSchema.find_by_username(username)
    if not user or not verify_password(password, user.password):
        return None
    return user

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Get curent user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception  
    except JWTError:
        raise credentials_exception

    user = UserSchema.find_by_username(username) 
    if user is None:
        raise credentials_exception
    return user

# Get current admin
async def get_current_admin_user(token: str = Depends(oauth2_scheme)):
    user = await get_current_user(token)
    if user.is_admin != True :
        raise HTTPException(
            status_code=403, 
            detail="Admin privileges required."
        )
    return user

# Function to check if the user is admin
async def verify_admin(user: UserSchema = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    # Ensure that the admin status is included in the JWT token payload
    to_encode.update({"is_admin": data.get("is_admin", False)})
    
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt