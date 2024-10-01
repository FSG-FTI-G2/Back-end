from typing import Annotated
import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.models.user import UserSchema  
from jose import JWTError, jwt
from app.controllers.auth_control import SECRET_KEY, ALGORITHM



security = HTTPBearer()
 

#Get user by token
def get_current_user_from_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):

    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Token is required",
        )

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )

    #Get id and expeir time
    username = data.get("sub") 
    exp = data.get("exp")

    if datetime.datetime.fromtimestamp(exp, tz=datetime.timezone.utc) < datetime.datetime.now(tz=datetime.timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired Token",
        )

    # Get info user
    user = UserSchema.find_by_username(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user