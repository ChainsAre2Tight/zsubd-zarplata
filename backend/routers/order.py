from fastapi import APIRouter, HTTPException

from datetime import date

from backend.models.order import OrderIn, OrderOut, OrderData, OrderList
from backend.auth import get_current_user
from backend.dependencies import get_db_connection


router = APIRouter(prefix='/order')

@router.post('/', status_code=201, response_model=OrderOut)
def create_order(
        employee_uuid: get_current_user,
        connection: get_db_connection,
        order: OrderIn
    ):
    if order.amount <= 0:
        raise HTTPException(status_code=400, detail='Order amount is invalid')
    
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO fulfilled_order (employee_id, amount) VALUES (%s, %s) RETURNING id',
        (employee_uuid.uuid, order.amount)
    )
    result = cursor.fetchone()
    connection.commit()
    return {'uuid': result[0]}

@router.get(
    '/',
    response_model=OrderList
)
def read_orders(
        employee: get_current_user,
        connection: get_db_connection,
    ) -> OrderList:

    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT id, amount, fullfillment_date
        FROM fulfilled_order
        WHERE employee_id = %s
            AND (fullfillment_date + '30 days'::interval) > CURRENT_DATE
        ORDER BY fullfillment_date
        ''',
        (employee.uuid,)
    )
    data: list[tuple[str, float, date]] = cursor.fetchall()
    results = [
        OrderData(
            uuid=order[0],
            amount=order[1],
            date=order[2].strftime('%Y-%m-%d'),
        ) for order in data
    ]
    return OrderList(orders=results)
