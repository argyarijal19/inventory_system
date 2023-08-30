from sqlalchemy import Column, MetaData, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class UserMdl(Base):
    __tablename__ = "users"
    id_user = Column(Integer, primary_key=True)
    nama_lengkap = Column(String(50))
    username = Column(String(20))
    password = Column(String(20))
