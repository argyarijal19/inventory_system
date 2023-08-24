from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BahanMdl(Base):
    __tablename__ = "bahan"
    id_bahan = Column(String(20), primary_key=True)
    nama_bahan = Column(String(50))
