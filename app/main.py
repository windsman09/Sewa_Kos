from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import kos
from fastapi import FastAPI, Request
from app.database import engine
from app import models
from fastapi import Form, File, UploadFile


models.Base.metadata.create_all(bind=engine)
# Init app
app = FastAPI(title="Website Sewa Kos")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Router
app.include_router(kos.router)
