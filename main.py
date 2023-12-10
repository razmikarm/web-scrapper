from parser import NewsParser
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    parser = NewsParser(
        base_url='https://news.am',
        path='/eng/'
    )
    data = parser.parse()

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request, 
            "articles": data,
        }
    )
