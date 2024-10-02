from typing import AnyStr, Dict
import os
from fastapi import HTTPException, status
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

class JWTProvider:
    '''
    Perform JWT encoding and decoding
    '''

    def __init__(self):
        self.secret = os.getenv("JWT_SECRET")
        self.algorithm = "HS256"  

    def encrypt(self, data: Dict) -> AnyStr:
        '''
        Encrypt data using JWT
        '''
        return jwt.encode(data, str(self.secret), algorithm=self.algorithm)

    def decrypt(self, token: AnyStr) -> Dict | None:
        '''
        Decode tokens using JWT
        '''
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Unable to verify information. {str(e)}"
            )
