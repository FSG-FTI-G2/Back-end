from datetime import datetime, timedelta, timezone
from app.models.user import UserSchema
from app.providers import encryptor

ACCESS_TOKEN_EXPIRE_DAYS = 30


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    '''
    Create jwt access token
    '''
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + \
            timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
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
