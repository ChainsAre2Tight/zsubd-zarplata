from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from backend.dependencies import get_db_cursor
from backend.auth import get_password_hash, create_access_token
from backend.models.auth import Token

router = APIRouter(prefix='/token')

@router.post('', response_model=Token)
async def login(
        cursor: get_db_cursor,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):

    def verify_user(cursor, username, hashed_pwd) -> tuple | None:
        print('...', username, hashed_pwd)
        cursor.execute(
            "SELECT employee_id FROM employee_user WHERE username = %s AND pwd = %s LIMIT 1",
            (username, hashed_pwd)
        )
        result = cursor.fetchone()
        return result

    employee_id = verify_user(
        cursor=cursor,
        username=form_data.username,
        hashed_pwd=get_password_hash(form_data.password)
    )
    print(employee_id)
    if employee_id is None:
        raise HTTPException(status_code=403, detail='Invalid username or password')
    
    access_token = create_access_token(
        data={'employeeUUID': employee_id, 'scope': 'employee'}
    )

    return {'access_token': access_token, 'token_type': 'bearer'}
