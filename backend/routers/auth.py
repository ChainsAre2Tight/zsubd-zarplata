from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from backend.dependencies import get_db_connection
from backend.auth import get_password_hash, create_access_token, verify_password
from backend.models.auth import Token

router = APIRouter(prefix='/token')

@router.post('', response_model=Token)
async def login(
        connection: get_db_connection,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):

    invalid_credentials = HTTPException(status_code=403, detail='Invalid username or password')

    def verify_user(cursor, username, hashed_pwd) -> tuple | None:
        cursor.execute(
            "SELECT employee_id, pwd FROM employee_user WHERE username = %s LIMIT 1",
            (username,)
        )
        result = cursor.fetchone()
        if result is None:
            raise invalid_credentials
        employee_id, hashed_pwd = result
        return employee_id, hashed_pwd

    employee_id, hashed_pwd = verify_user(
        cursor=connection.cursor(),
        username=form_data.username,
        hashed_pwd=get_password_hash(form_data.password)
    )

    if employee_id is None or not verify_password(form_data.password, hashed_pwd):
        raise invalid_credentials
    
    access_token = create_access_token(
        data={'employeeUUID': employee_id, 'scope': 'employee'}
    )

    return {'access_token': access_token, 'token_type': 'bearer'}
