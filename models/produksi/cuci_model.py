from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CuciMdl(Base):
    __tablename__ = "tabel_cuci"
    id_cucian = Column(Integer, primary_key=True)
    id_produksi = Column(String(20))
    id_vendor = Column(Integer)
    # tanggal_cuci = Column(DateTime)
    # tanggal_selesai = Column(DateTime)
