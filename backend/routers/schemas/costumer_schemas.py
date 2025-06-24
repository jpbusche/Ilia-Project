from pydantic import BaseModel


class CostumerCreate(BaseModel):
    name: str
    email: str
    password: str

class CostumerLogin(BaseModel):
    email: str
    password: str