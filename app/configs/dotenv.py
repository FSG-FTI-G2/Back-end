import dotenv
import logging


logger = logging.getLogger("uvicorn.info")


def load_enviroment_variables():
    dotenv.load_dotenv(dotenv.find_dotenv())

    # Log variables
    logger.info("🔒 Environment loaded")

    return True
