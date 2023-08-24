from pydantic import BaseModel


class Bahan(BaseModel):
    id_bahan: str
    nama_bahan: str


class UpdateBahan(BaseModel):
    nama_bahan: str
