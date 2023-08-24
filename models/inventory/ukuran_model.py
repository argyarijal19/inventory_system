from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UkuranMdl(Base):
    __tablename__ = "ukuran"
    id_ukuran = Column(Integer, primary_key=True)
    nama_ukuran = Column(String(5))
