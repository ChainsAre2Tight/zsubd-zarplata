from fastapi import APIRouter

import backend.models.employee as models


router = APIRouter(prefix='/employee')


@router.post('', status_code=201, response_model=models.EmployeeResponse)
def create_employee(data: models.EmployeeToCreate):
    return {'employee_uuid': 'test'}
