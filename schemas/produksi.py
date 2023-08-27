from pydantic import BaseModel
from datetime import datetime


class ProduksiScm(BaseModel):
    id_produksi: str
    id_inv: str
    qty_pembuatan: int
    tanggal_pembuatan: datetime
