from fastapi import FastAPI

import backend.routers.employee as employee


app = FastAPI()

app.include_router(employee.router)
