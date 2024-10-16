from pydantic import BaseModel
from typing import Optional


class EmployeeToCreate(BaseModel):
    fio: str
    payment_mathod: Optional[str] = None
    receipt_address: Optional[str] = None


class EmployeeResponse(BaseModel):
    employee_uuid: str

class EmployeeUser(BaseModel):
    uuid: str
