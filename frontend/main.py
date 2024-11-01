from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://zarplata.zsubd",
    "http://localhost:5010",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory='templates')

@app.get('/')
def render_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
    )

@app.get('/login')
def render_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='login-window.html',
    )

@app.middleware('http')
async def add_nocache_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers.update({"Cache-Control": 'no-cache'})
    return response

app.mount('/static', StaticFiles(directory='static'), name='static')
