from .db import DatabaseProvider
from .encryption import EncryptionProvider

encryptor = EncryptionProvider()

user_db = DatabaseProvider("users")
file_db = DatabaseProvider("files")
