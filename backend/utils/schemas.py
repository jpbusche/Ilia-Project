from pydantic import BaseModel
from typing import Optional


class Costumers(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class Product(BaseModel):
    id: str
    quantity: Optional[int] = 1

class Order(BaseModel):
    id: str