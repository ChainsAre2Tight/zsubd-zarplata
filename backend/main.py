from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

import backend.routers.employee as employee
import backend.routers.auth as auth
import backend.routers.order as order


app = FastAPI()

origins = [
    "http://zarplata.zsubd",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_router = APIRouter(prefix='/api/v1')
base_router.include_router(employee.router)
base_router.include_router(auth.router)
base_router.include_router(order.router)

app.include_router(base_router)
