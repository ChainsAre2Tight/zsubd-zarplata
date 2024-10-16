from fastapi import FastAPI, APIRouter

import backend.routers.employee as employee


app = FastAPI()

base_router = APIRouter(prefix='/api/v1')
base_router.include_router(employee.router)

app.include_router(base_router)
