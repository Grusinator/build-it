from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from wkg.geometry_parser import load_geometries_from_file

templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class Box(BaseModel):
    width: float
    height: float
    depth: float


@app.get("/", response_class=HTMLResponse)
async def serve_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/box")
def get_box():
    # Sample data; this could be fetched from a database or another source.
    return Box(width=1, height=2, depth=3)


@app.get("/collection")
def get_collection():
    boxes = load_geometries_from_file("wkg/example_files/house.wkg")
    return JSONResponse(content=[box.model_dump() for box in boxes])