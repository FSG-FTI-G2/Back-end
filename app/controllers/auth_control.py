from datetime import datetime, timedelta
from app.models.user import UserSchema
from app.providers import encryptor

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    '''
    Create jwt access token
    '''
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return encryptor.encrypt(data)


async def authenticate_user(username: str, password: str):
    '''
    Authenticate user
    '''
    user = UserSchema.find_by_username(username)
    if not user or not encryptor.match_hash(password, user.password):
        return None
    return user
