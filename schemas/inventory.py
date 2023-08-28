from pydantic import BaseModel


class InvetoryPostBahan(BaseModel):
    id_ukuran: int
    nama_produk: str
    harga_produk: int
    id_inventory: str
    id_bahan: str


class UpdateInventory(BaseModel):
    harga_produk: int
    nama_produk: str
