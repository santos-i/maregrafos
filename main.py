from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    from teste import testando
    fig = testando()
    return templates.TemplateResponse('home.html', context={'request':request, 'fig':fig})


@app.get('/maregrafo-{id}', response_class=HTMLResponse)
def showMaregrafo(request: Request, id):
    return templates.TemplateResponse(f'maregrafo-{id}.html', context={'request':request})