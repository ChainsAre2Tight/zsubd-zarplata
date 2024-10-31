from fastapi import APIRouter, HTTPException, status

from datetime import datetime, timedelta, date

from backend.auth import get_current_user
from backend.dependencies import get_db_connection
from backend.models.vacation import VacationIn, VacationOut

router = APIRouter(prefix='/vacation')
MAXIMUM_VACATION_DURATION = 35

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=VacationOut,
)
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

    data: list[tuple[date, date]] = cursor.fetchall()
    current_duration = sum([(vac[1] - vac[0]).days for vac in data])

    proposed_duration = (end_date - begin_date).days
    remaining_duration = MAXIMUM_VACATION_DURATION - (current_duration + proposed_duration)
    if remaining_duration < 0:
        raise HTTPException(status_code=400, detail='Reached maximum vacation duration this year duration')
    
    # validate non-overlapping nature of vacations
    # what we have is an list of dates in an ascending order
    # traverse it, if we get start_date, increment state by 1
    # if we get end_date, decrement it
    # if at some point state is not 0 or 1, we have an overlap
    array = [(1, begin_date.toordinal()), (-1, end_date.toordinal())]
    for start, end in data:
        array.append((1, start.toordinal()))
        array.append((-1, end.toordinal()))
    array.sort(key=lambda x: x[1])
    state = 0
    for i in array:
        state += i[0]
        if state < 0 or state > 1:
            raise HTTPException(
                status_code=400,
                detail='Your vacation overlaps with another one of yours'
            )

    cursor.execute(
        'INSERT INTO vacation (employee_id, begin_date, end_date) VALUES (%s, %s, %s) RETURNING id',
        (employee.uuid, begin_date, end_date)
    )
    id = cursor.fetchone()[0]

    connection.commit()
    return {
        'vacation_id': id,
        'remaining_duration': remaining_duration,
        'max_duration': MAXIMUM_VACATION_DURATION,
    }
