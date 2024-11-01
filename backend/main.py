from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.middleware.cors import CORSMiddleware

import backend.routers.employee as employee
import backend.routers.auth as auth
import backend.routers.vacation as vacation
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

@app.middleware('http')
async def add_nocache_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers.update({"Cache-Control": 'no-cache'})
    return response

base_router = APIRouter(prefix='/api/v1')
base_router.include_router(employee.router)
base_router.include_router(auth.router)
base_router.include_router(vacation.router)
base_router.include_router(order.router)

app.include_router(base_router)
