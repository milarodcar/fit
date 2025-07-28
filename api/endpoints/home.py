from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()

templates = Jinja2Templates(directory=str(Path(__file__).parent.parent.parent / "static" / "templates"))

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("clients/home.html", {"request": request})