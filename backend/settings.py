import os

SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "dev")


class CreateException(Exception):
    pass
