from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated

from backend.models.employee import EmployeeUser

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
_token = Annotated[str, Depends(_oauth2_scheme)]

def _fake_decode_token(token: str) -> EmployeeUser:
    return EmployeeUser(
        uuid=token,
    )

def _get_current_user(token: _token) -> EmployeeUser:
    return _fake_decode_token(token=token)


get_current_user = Annotated[EmployeeUser, Depends(_get_current_user)]
