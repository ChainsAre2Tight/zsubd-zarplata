from pydantic import BaseModel

class Order(BaseModel):
    amount: float
