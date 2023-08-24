from sqlalchemy import Column, MetaData, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BahanMdl(Base):
    __tablename__ = "pos"
    id_pos = Column(Integer, primary_key=True)
    id_inv = Column(String(20))
    total_qty = Column(Integer)
    total_income = Column(Integer)
