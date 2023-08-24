from pydantic import BaseModel


class InvetoryPostBahan(BaseModel):
    id_inventory: str
    id_bahan: str


class InventoryUpdateProduk(BaseModel):
    id_ukuran: int
    nama_produk: str
    harga_produk: int
