from pydantic import BaseModel

class OrderIn(BaseModel):
    amount: float

class OrderOut(BaseModel):
    uuid: str

class OrderData(BaseModel):
    uuid: str
    amount: float
    date: str

class OrderList(BaseModel):
    orders: list[OrderData]