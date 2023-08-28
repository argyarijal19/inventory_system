from fastapi import APIRouter
from repository.produksi.vendor_repo import *
from sqlalchemy.exc import IntegrityError
from helper.response import *

vendor = APIRouter(prefix="/vendor", tags=["Vendor Detail"])


@vendor.get("/")
async def get_all_vendor():
    data = get_vendor()
    if data:
        return success_get_data(data)

    return get_data_null("Tidak Dapat Ditemukan Data Vendor")


@vendor.get("/{id_vendor}")
async def get_vendor_data_by_id(id_vendor: int):
    data_vendor = get_vendor_by_id(id_vendor)
    if data_vendor:
        return success_get_data(data_vendor)

    return get_data_null(f"Data Dengan ID {id_vendor} Tidak Ditemukan")


@vendor.post("/create_vendor")
async def create_vendor_post(ven: CreateVendor):
    try:
        create_data = create_vendor(ven)
        if create_data:
            return success_post_data(1, "Vendor Berhasil Dibuat")
        else:
            return post_data_fail("Gagal Membuat Vendor Data")
    except IntegrityError:
        return post_data_fail("ID tidak Boleh sama")

    except:
        return post_data_fail("Gagal Membuat Data")


@vendor.put("/update_vendor/{id_vendor}")
async def update_data_vendor(ven: CreateVendor, id_vendor: int):
    try:
        update_data = update_vendor(ven, id_vendor)
        if update_data:
            return success_post_data(1, "Berhasil Mengupadate vendor")

        return post_data_fail("Gagal Mengupdate Data Vendor")
    except:
        return post_data_fail("Gagal Mengupdate Data Vendor")


@vendor.delete("/delete_vendor/{id_vendor}")
async def delete_vendor_data(id_vendor: int):
    delete = delete_vendor(id_vendor)
    if delete:
        return success_post_data(1, "Berhasil Delete Data")

    return get_data_null("ID Vendor Tidak Ditemukan")
