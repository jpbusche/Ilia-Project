from pydantic import BaseModel


class Costumers(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str