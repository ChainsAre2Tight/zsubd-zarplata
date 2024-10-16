from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

router = APIRouter(prefix='/token')

@router.post('')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not (form_data.username == 'test' and form_data.password == 'mypwd'):
        raise HTTPException(status_code=400, detail='Incorrect user or password')
    return {'access_token': 'test-token', 'token_type': 'bearer'}
