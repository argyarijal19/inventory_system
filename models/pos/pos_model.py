from sqlalchemy import Column, MetaData, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class PosMdl(Base):
    __tablename__ = "pos"
    id_pos = Column(Integer, primary_key=True)
    id_inv = Column(String(20))
    total_qty = Column(Integer)
    total_income = Column(Integer)
    tanggal_barang_out = Column(DateTime, default=datetime.now().date())
