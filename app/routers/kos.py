from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from fastapi.staticfiles import StaticFiles

router = APIRouter()

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    kos = db.query(models.Kos).all()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "kos": kos
        }
    )


@router.get("/detail/{kos_id}")
def detail(kos_id: int, request: Request, db: Session = Depends(get_db)):
    kos = db.query(models.Kos).filter(models.Kos.id == kos_id).first()
    return templates.TemplateResponse(
        "detail_kos.html",
        {
            "request": request,
            "kos": kos
        }
    )
