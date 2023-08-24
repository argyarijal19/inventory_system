from fastapi import APIRouter
from repository.barang_mentah.bahan_repo import *
from sqlalchemy.exc import IntegrityError
from helper.response import *
from helper.make_qrcode import Generate_qrcode
from schemas.bahan import *

bahan = APIRouter(prefix="/bahan", tags=["Bahan Detail"])


@bahan.get("/")
async def get_bahan_all() -> dict:
    bahan = get_all_bahan()
    if bahan:
        return success_get_data(bahan)
    return get_data_null("tidak ditemukan data bahan")


@bahan.get("/{id_bahan}")
async def get_bahan_by_id(id_bahan: str) -> dict:
    bahan = bahan_by_id(id_bahan)
    if bahan:
        qrcode = Generate_qrcode(bahan["id_bahan"])
        data_response = {
            "id_bahan": bahan["id_bahan"],
            "nama_bahan": bahan["nama_bahan"],
            "qrcode_base64": qrcode
        }
        return data_response
    return get_data_null("tidak ditemukan data bahan")


@bahan.put("/update/{id_bahan}")
async def put_data_bahan(nama: UpdateBahan, id_bahan: str):
    try:
        update = update_bahan(nama, id_bahan)
        if update:
            return success_post_data(nama.nama_bahan, "Data bahan Berhasil Dirubah")
        return post_data_fail("ID bahan tidak ditemukan")
    except IntegrityError:
        return post_data_fail("Data ada yang salah")


@bahan.post("/post_bahan")
async def post_bahan_mentah(bahan: Bahan):
    try:
        post_data = create_bahan(bahan)
        if post_data:
            return success_post_data("Data Berhasil Disimpan")
    except IntegrityError:
        return post_data_fail("Id Bahan Tidak Boleh Sama")


@bahan.delete("/del_bahan/{id_bahan}")
async def delete_data_bahan(id_bahan: str):
    try:
        data_delete = delete_bahan(id_bahan)
        if data_delete:
            return success_get_data("Data Berhasil Dihpaus")
        return get_data_null("ID bahan tidak ditemukan")
    except IntegrityError:
        return get_data_null("data tidak dapat dihapus")
