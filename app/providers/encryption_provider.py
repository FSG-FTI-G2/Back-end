from typing import AnyStr, Dict
import os
import bcrypt
from jose import jwt, JWTError
from fastapi import HTTPException, status


class EncryptionProvider:
    '''
    Perform hash, encrypt, and decrypt operations
    '''

    def __init__(self):
        self.secret = os.getenv("JWT_SECRET")
        self.algorithm = "HS256"

    def hash(self, data: AnyStr) -> AnyStr:
        '''
        Hash data using bcrypt
        '''
        return bcrypt.hashpw(data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def match_hash(self, data: AnyStr, hashed_data: AnyStr) -> bool:
        '''
        Compare hashed data with original data
        '''
        return bcrypt.checkpw(data.encode('utf-8'), hashed_data.encode('utf-8'))

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
