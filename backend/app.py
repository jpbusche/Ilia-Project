from mongoengine import connect, disconnect
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from routers.costumer import costumers
from routers.product import products
from routers.order import orders
from settings import MONGO_URL, MONGO_DB
from utils.exceptions import APIException
from database.populate import populate_database

async def lifespan(app: FastAPI):
    connect(host=MONGO_URL, db=MONGO_DB)
    populate_database()
    yield
    disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(costumers, prefix="/costumers", tags=["costumers"])
app.include_router(products, prefix="/products", tags=["products"])
app.include_router(orders, prefix="/orders", tags=["orders"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(APIException)
async def handle_auth_exception(request: Request, exception: APIException):
    return JSONResponse(status_code=exception.status_code, content={"message": exception.message, "success": False})
