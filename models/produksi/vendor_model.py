from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class VendorMdl(Base):
    __tablename__ = "vendor"
    id_vendor = Column(Integer, primary_key=True)
    nama_vendor = Column(String(20))
    jenis_vendor = Column(String(20))
