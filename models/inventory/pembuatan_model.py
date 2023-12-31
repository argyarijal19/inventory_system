from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class PembuatanMdl(Base):
    __tablename__ = "pembuatan"
    id_pembuatan = Column(Integer, primary_key=True)
    id_inv = Column(String(20))
    interval_pembuatan = Column(Integer)
    qty_pembuatan = Column(Integer)
    tanggal_pembuatan = Column(DateTime)
    tanggal_selesai = Column(DateTime)