from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class InventoryMdl(Base):
    __tablename__ = "inventory"
    id_inv = Column(String(20), primary_key=True)
    id_bahan = Column(String(20))
    id_ukuran = Column(Integer)
    nama_produk = Column(String(50))
    harga_produk = Column(Integer)
    qty = Column(Integer)
    qty_washing = Column(Integer)
    qty_final = Column(Integer)
    status_trc = Column(String(2))
    tanggal_mulai_jait = Column(DateTime)
    tanggal_produk_jadi = Column(DateTime)
