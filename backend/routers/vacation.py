from fastapi import APIRouter, HTTPException, status

from datetime import datetime, timedelta

from backend.auth import get_current_user
from backend.dependencies import get_db_connection
from backend.models.vacation import VacationIn

router = APIRouter(prefix='/vacation')
MAXIMUM_VACATION_DURATION = 35

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_vacation(
        employee: get_current_user,
        connection: get_db_connection,
        vacation: VacationIn
    ):
    cursor = connection.cursor()

    begin_date = datetime.date(datetime.fromisoformat(vacation.begin_date))
    end_date = datetime.date(datetime.fromisoformat(vacation.end_date))

    # validate begin_date in before end_date
    if begin_date >= end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Vacation ends before it starts :('
        )

    # validate vacation starts the same year it ends
    if begin_date.year != end_date.year:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Vacation should end the same year it started'
        )

    # validate vacation is at leats 60 days into future
    today = datetime.date(datetime.now())
    next_year = today + timedelta(days=365)
    if (begin_date - today).days < 60:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Vacation should start at least 60 days from now'
        )
    
    # validate vacation is for this year or next
    match begin_date.year:
        case today.year:
            selected_year = today
        case next_year.year:
            selected_year = next_year
        case _:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Vacations can only be reserved for current or next year'
        )

    cursor.execute(
        """SELECT begin_date, end_date FROM vacation WHERE employee_id = %s
        AND DATE_PART('year', %s::date) = DATE_PART('year', begin_date::date)""",
        (employee.uuid, selected_year)
    )

    data = cursor.fetchall()
    current_duration = sum([(vac[1] - vac[0]).days for vac in data])

    proposed_duration = (end_date - begin_date).days
    if current_duration + proposed_duration > MAXIMUM_VACATION_DURATION:
        raise HTTPException(status_code=400, detail='Reached maximum vacation duration this year duration')
    
    cursor.execute(
        'INSERT INTO vacation (employee_id, begin_date, end_date) VALUES (%s, %s, %s) RETURNING id',
        (employee.uuid, begin_date, end_date)
    )
    id = cursor.fetchone()[0]

    connection.commit()
    return {'vacation_id': id}
