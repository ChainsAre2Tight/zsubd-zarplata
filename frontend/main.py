from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='templates')

@app.get('/')
def render_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
    )
