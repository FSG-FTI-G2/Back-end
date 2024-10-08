from .db import DatabaseProvider
from .encryption import EncryptionProvider

encryptor = EncryptionProvider()

user_db = DatabaseProvider("users")
file_db = DatabaseProvider("files")
llm_config_db = DatabaseProvider("llm_config")
