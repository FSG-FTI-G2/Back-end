import os
import dotenv
import logging


def load_enviroment_variables():
    dotenv.load_dotenv(dotenv.find_dotenv())

    # Log variables
    logging.info("Environment loaded", os.environ)

    return True
