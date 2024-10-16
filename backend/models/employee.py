from pydantic import BaseModel
from typing import Optional


class EmployeeData(BaseModel):
    fio: str
    payment_mathod: str
    receipt_address: str


class EmployeeResponse(BaseModel):
    employee_uuid: str

class EmployeeUser(BaseModel):
    uuid: str
