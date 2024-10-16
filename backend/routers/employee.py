from fastapi import APIRouter

import backend.models.employee as models
from backend.dependencies import get_db_cursor
from backend.auth import get_current_user

router = APIRouter(prefix='/employee')


@router.post('', status_code=201, response_model=models.EmployeeResponse)
def create_employee(
        cursor: get_db_cursor,
        data: models.EmployeeData,
    ):
    cursor.execute('insert into employee(fio) VALUES (%s) RETURNING id', (data.fio, ))
    id = cursor.fetchone()[0]
    return {'employee_uuid': id}

@router.get('/me', response_model=models.EmployeeData)
def read_current_employee(
        current_user: get_current_user,
        cursor: get_db_cursor
    ):
    cursor.execute(
        'SELECT fio, payment_method, receipt_address FROM employee WHERE id = %s LIMIT 1',
        (current_user.uuid, )
    )
    data = cursor.fetchone()
    assert data is not None, 'got empty employee from db'
    return {
        'fio': data[0],
        'payment_mathod': data[1],
        'receipt_address': data[2],
    }
