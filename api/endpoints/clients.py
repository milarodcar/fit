from pathlib import Path
from typing import Optional
from db.database import get_db
from sqlalchemy.orm import Session
from api.schemas import ClientCreate
from fastapi.templating import Jinja2Templates
from services.client_service import ClientService
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Depends, Request, Form, HTTPException

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent.parent / "static" / "templates"))

@router.get("/", response_class=HTMLResponse)
async def list_clients(
    request: Request,
    name: str = None,
    db: Session = Depends(get_db)
):
    service = ClientService(db)
    clients = service.get_clients_filtered(name=name)
    all_objectives = service.get_all_objectives() if hasattr(service, 'get_all_objectives') else []
    
    return templates.TemplateResponse(
        "clients/clients.html",
        {
            "request": request,
            "clients": clients,
            "all_objectives": all_objectives,
            "current_filter": name or ""
        }
    )

@router.get("/new", response_class=HTMLResponse)
async def new_client_form(request: Request):
    return templates.TemplateResponse("clients/new.html", {"request": request})

@router.post("/")
async def create_client(
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    objectives: str = Form(...),
    phone_number: str = Form(...),
    training_type: str = Form(...),
    service: str = Form(...),
    observations: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    client_obj = ClientCreate(
        name=name,
        age=age,
        weight=weight,
        objectives=objectives.split(","),
        phone_number=phone_number,
        training_type=training_type,
        service=service,
        observations=observations
    )
    
    client_service = ClientService(db)
    client_service.create_client(client_obj)
    return RedirectResponse(url="/clients", status_code=303)

@router.post("/{client_id}/delete", response_class=RedirectResponse)
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    service = ClientService(db)
    if not service.delete_client(client_id):
        raise HTTPException(status_code=404, detail="Client not found")
    return RedirectResponse(url="/clients", status_code=303)

@router.get("/{client_id}/edit", response_class=HTMLResponse)
async def edit_client_form(client_id: int, request: Request, db: Session = Depends(get_db)):
    service = ClientService(db)
    client = service.get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return templates.TemplateResponse("clients/new.html", {
        "request": request,
        "client": client,
        "is_edit": True
    })

@router.post("/{client_id}/edit")
async def update_client(
    client_id: int,
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    objectives: str = Form(...),
    phone_number: str = Form(...),
    training_type: str = Form(...),
    service: str = Form(...),
    observations: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    updated_data = ClientCreate(
        name=name,
        age=age,
        weight=weight,
        objectives=objectives.split(","),
        phone_number=phone_number,
        training_type=training_type,
        service=service,
        observations=observations
    )

    service = ClientService(db)
    if not service.update_client(client_id, updated_data):
        raise HTTPException(status_code=404, detail="Client not found")

    return RedirectResponse(url="/clients", status_code=303)
