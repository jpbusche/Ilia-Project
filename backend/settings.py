import os

# Mongo Configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "dev")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta")
EXPIRE_TIME = int(os.getenv("EXPIRE_TIME", '60'))


class CostumerException(Exception):
    pass
