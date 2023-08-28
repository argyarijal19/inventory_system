from pydantic import BaseModel
from datetime import datetime


class ProduksiScm(BaseModel):
    id_produksi: str
    id_vendor: int
    id_inv: str
    qty_pembuatan: int
    tanggal_pembuatan: str


class CreateJaitan(BaseModel):
    id_produksi: str
    id_vendor: int


class UpdateProduksi(BaseModel):
    qty: int


class CreateCuci(BaseModel):
    id_produksi: str
    id_vendor: int


class CreateVendor(BaseModel):
    nama_vendor: str
    jenis_vendor: str
