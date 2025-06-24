from mongoengine import connect
from fastapi import FastAPI

from routers.costumer import costumers
from settings import MONGO_URL, MONGO_DB


app = FastAPI()
app.include_router(costumers, prefix="/costumers", tags=["costumers"])
connect(host=MONGO_URL, db=MONGO_DB)
