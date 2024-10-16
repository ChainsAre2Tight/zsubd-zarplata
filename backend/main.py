from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

import backend.routers.employee as employee


app = FastAPI()

origins = [
    "http://zarplata.zsubd",
    "http://localhost:5000",
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

app.include_router(base_router)
