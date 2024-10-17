from pydantic import BaseModel

class OrderIn(BaseModel):
    amount: float

class OrderOut(BaseModel):
    uuid: str
