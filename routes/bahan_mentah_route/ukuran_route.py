from fastapi import APIRouter
from repository.barang_mentah.ukuran_repo import *
from sqlalchemy.exc import IntegrityError
from helper.response import *
from schemas.ukuran import *

ukuran = APIRouter(prefix="/ukuran", tags=["Ukuran Detail"])


@ukuran.get("/")
async def get_bahan_all() -> dict:
    ukuran = get_all_ukuran()
    if ukuran:
        return success_get_data(ukuran)
    return get_data_null("tidak ditemukan data ukuran")


@ukuran.get("/{ukuran_id}")
async def get_bahan_by_id(ukuran_id: str) -> dict:
    ukuran_data = ukuran_by_id(ukuran_id)
    if ukuran_data:
        return ukuran_data
    return get_data_null("ID ukuran tidak ditemukan")


@ukuran.put("/update/{ukuran_id}")
async def put_data_bahan(nama: Ukuran, ukuran_id: str):
    try:
        update = update_ukuran(nama, ukuran_id)
        if update:
            return success_post_data(nama.nama_ukuran, "Data bahan Berhasil Dirubah")
        return post_data_fail("ID ukuran tidak ditemukan")
    except IntegrityError:
        return post_data_fail("nama ukuran Tidak Boleh Sama")


@ukuran.post("/post_Ukuran")
async def post_bahan_mentah(ukuran: Ukuran):
    try:
        if len(ukuran.nama_ukuran) > 5:
            return post_data_fail("Ukuran tidal boleh lebih dari 5 karakter")

        post_data = create_ukuran(ukuran)
        if post_data:
            return success_post_data(1, "Data Berhasil Disimpan")
    except IntegrityError:
        return post_data_fail("nama ukuran Tidak Boleh Sama")
    except Exception as e:
        return post_data_fail(e)


@ukuran.delete("/del_ukuran/{id_ukuran}")
async def delete_data_ukuran(id_ukuran: str):
    try:
        data_delete = delete_ukuran(id_ukuran)
        if data_delete:
            return success_get_data("Data Berhasil Dihpaus")
        return get_data_null("ID ukuran tidak ditemukan")
    except IntegrityError:
        return get_data_null("data tidak dapat dihapus")
