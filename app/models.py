from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Kos(Base):
    __tablename__ = "kos"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    alamat = Column(String)
    harga = Column(Integer)
    deskripsi = Column(String)
    image = Column(String)
    tersedia = Column(Boolean, default=True)
