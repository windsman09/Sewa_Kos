from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi import Form, File, UploadFile
from fastapi.responses import RedirectResponse


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
def home(
    request: Request,
    q: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Kos)

    if q:
        query = query.filter(
            models.Kos.nama.ilike(f"%{q}%") |
            models.Kos.alamat.ilike(f"%{q}%")
        )

    kos = query.all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "kos": kos,
            "q": q
        }
    )



@router.get("/tambah")
def form_tambah(request: Request):
    return templates.TemplateResponse(
        "tambah.html",
        {"request": request}
    )
@router.post("/tambah")
def simpan_kos(
    nama: str = Form(...),
    alamat: str = Form(...),
    harga: int = Form(...),
    deskripsi: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    kos = models.Kos(
        nama=nama,
        alamat=alamat,
        harga=harga,
        deskripsi=deskripsi
    )

    db.add(kos)
    db.commit()
    db.refresh(kos)

    return RedirectResponse("/", status_code=303)
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