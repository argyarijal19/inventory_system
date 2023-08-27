from pydantic import BaseModel


class ProduksiScm(BaseModel):
    id_produksi: str
    id_vendor: int
    id_inv: str
    qty_pembuatan: int
