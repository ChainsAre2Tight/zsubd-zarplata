from fastapi import APIRouter, HTTPException

from backend.models.order import OrderIn, OrderOut
from backend.auth import get_current_user
from backend.dependencies import get_db_cursor


router = APIRouter(prefix='/order')

@router.post('/', status_code=201, response_model=OrderOut)
def create_order(
        employee_uuid: get_current_user,
        cursor: get_db_cursor,
        order: OrderIn
    ):
    if order.amount <= 0:
        raise HTTPException(status_code=400, detail='Order amount is invalid')
    
    cursor.execute(
        'INSERT INTO fulfilled_order (employee_id, amount) VALUES (%s, %s) RETURNING id',
        (employee_uuid, order.amount)
    )
    result = cursor.fetchone()
    return {'uuid': result[0]}
