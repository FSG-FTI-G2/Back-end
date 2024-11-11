from typing import Annotated
import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.models.user_schema import UserSchema
from app.providers import encryptor


security = HTTPBearer()


# Get user by token
def auth_user_middleware(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):

    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Token is required",
        )

    data = encryptor.decrypt(token)

    # Get id and expired time
    user_id = data.get("uid")
    exp = data.get("exp")

    if datetime.datetime.fromtimestamp(exp, tz=datetime.timezone.utc) < datetime.datetime.now(tz=datetime.timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired Token",
        )

    # Get info user
    user = UserSchema.find_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
