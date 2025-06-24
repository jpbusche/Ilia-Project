from mongoengine import connect
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers.costumer import costumers
from settings import MONGO_URL, MONGO_DB
from utils.exceptions import AuthException


app = FastAPI()
app.include_router(costumers, prefix="/costumers", tags=["costumers"])
connect(host=MONGO_URL, db=MONGO_DB)


@app.exception_handler(AuthException)
async def handle_auth_exception(request: Request, exception: AuthException):
    return JSONResponse(status_code=exception.status_code, content={"message": exception.message, "success": False})
