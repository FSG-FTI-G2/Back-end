'''
Migration script for databases
'''
from app.models.user import UserSchema
from app.providers import encryptor, vector_db
from app.utils.logger import get_logger

logger = get_logger("MIGRATE", color=1)

# ---------------------------------------------------------
# Variables
# ---------------------------------------------------------
USERNAME = "admin"
PASSWORD = "admin1111"


def auto_migrate():
    logger("⚙️ Auto migrating database...")

    # Create Admin User as default user
    admin = UserSchema.find_by_username("admin")
    if not admin:
        admin = UserSchema(
            username=USERNAME,
            password=encryptor.hash(PASSWORD),
        ).create()

    # Create Qdrant collection by user id
    vector_db.create_collection(admin.id)
