# from .db import DatabaseProvider


# user_db = DatabaseProvider("users")


from app.providers.db import QdrantProvider

user_db = QdrantProvider("users")