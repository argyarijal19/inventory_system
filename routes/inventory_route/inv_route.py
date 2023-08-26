import re
from fastapi import APIRouter
from repository.inventory.inventory_repo import *
from repository.barang_mentah.bahan_repo import bahan_by_id
from repository.barang_mentah.ukuran_repo import ukuran_by_id
from sqlalchemy.exc import IntegrityError
from helper.response import *
from helper.make_qrcode import Generate_qrcode
from schemas.bahan import *

inv = APIRouter(prefix="/inv", tags=["Inventory Detail"])


@inv.get("/")
async def get_all_data_inventory() -> dict:
    inv = get_all_inventory()
    if inv:
        return success_get_data(inv)
    return get_data_null("tidak ditemukan data bahan")


@inv.get("/produk_jadi")
async def get_all_data_produk_jadi() -> dict:
    inv = get_all_produk_jadi()
    if inv:
        return success_get_data(inv)
    return get_data_null("tidak ditemukan data bahan")


@inv.get("/{id_inv}")
async def get_data_inventory_by_id(id_inv: str) -> dict:
    inv = get_inventory_by_id(id_inv)
    if inv:
        qrcode = Generate_qrcode(inv["id_inv"])
        response_data = {
            "id_inv": inv["id_inv"],
            "id_bahan": inv["id_bahan"],
            "nama_produk": inv["nama_produk"],
            "harga_produk": inv["harga_produk"],
            "qty": inv["qty"],
            "nama_bahan": inv["nama_bahan"],
            "ukuran": inv["ukuran"],
            "status": inv["status_trc"],
            "qrcode": qrcode
        }
        return success_get_data(response_data)
    return get_data_null("tidak ditemukan data bahan")


@inv.post("/post_inv")
async def post_inventory_data(inv: InvetoryPostBahan):
    id_bahan = bahan_by_id(inv.id_bahan)
    if id_bahan:
        # try:
        pattern = r'^[A-Z]{2}_\d{3}[A-Z]{2}$'
        if re.match(pattern, inv.id_inventory):
            chek_data = get_inventory_by_id(inv.id_inventory)
            if chek_data:
                if chek_data["status_trc"] != "3":
                    return post_data_fail("Produk tersebut masih dalam proses")

            postdata_inv = create_inventory(inv)
            if postdata_inv:
                return success_post_data(1, "Data Berhasil Disimpan")
            return postdata_inv
        else:
            return post_data_fail("ID harus di awali denga 2 huruf kemudian underscorenya kemudian 3 digit angka kemudiaan 2 huruf lagi CONTOH: KM_001PL")
        # except IntegrityError:
        #     return post_data_fail("ID inventory tidak boleh sama")
        # except Exception as e:
        #     return e
    return post_data_fail("Data Bahan tidak ditemukan")


@inv.put("/update_jahitan/{inv_id}")
async def put_data_tracking_jahitan(inv_id: str):
    # cek_data = get_inventory_by_id(inv_id)
    try:
        update = update_jahitan(inv_id)
        if update:
            return success_post_data(True, "Data Berhasil Di Update")
        return update
    except IntegrityError:
        return post_data_fail("nama inventory Tidak Boleh Sama atau ukuran tidak valid")


@inv.put("/update_cuci/{inv_id}")
async def put_data_tracking_cucian(inv_id: str):
    cek_data = get_inventory_by_id(inv_id)
    if cek_data["qty_washing"] is None:
        try:
            update = update_cucian(inv_id, cek_data["status_trc"])
            if update:
                return success_post_data(True, "Data Berhasil Di Update")
            return post_data_fail("ID inventory tidak ditemukan")
        except IntegrityError:
            return post_data_fail("nama inventory Tidak Boleh Sama")
    else:
        if int(cek_data["qty_washing"]) > int(cek_data["qty"]):
            return post_data_fail("Produk tidak tercatat saat penjahitan")

        elif int(cek_data["qty_washing"]) == int(cek_data["qty"]) - 1:
            try:
                update = update_cucian(inv_id, "3")
                if update:
                    update_pembuatan_check = update_pembuatan(
                        cek_data["id_inv"], (cek_data["qty_washing"]) + 1)
                    if update_pembuatan_check:
                        return success_post_data(True, "Data Berhasil Di Update")
                return post_data_fail("ID inventory tidak ditemukan")
            except IntegrityError:
                return post_data_fail("nama inventory Tidak Boleh Sama")

        elif int(cek_data["qty_washing"]) < int(cek_data["qty"]):
            try:
                update = update_cucian(inv_id, "2")
                if update:
                    return success_post_data(True, "Data Berhasil Di Update")
                return post_data_fail("ID inventory tidak ditemukan")
            except IntegrityError:
                return post_data_fail("nama inventory Tidak Boleh Sama")
        else:
            return post_data_fail("Produk Terleat dari Proses Pencucian")

# @inv.put("/update_produk/{inv_id}")
# async def put_data_tracking_gudang(inv_id: str):
#     cek_data = get_inventory_by_id(inv_id)
#     if cek_data["qty_washing"] is None:
#         try:
#             update = update_produk(inv_id)
#             if update:
#                 return success_post_data(True, "Data Berhasil Di Update")
#             return post_data_fail("ID inventory tidak ditemukan")
#         except IntegrityError:
#             return post_data_fail("ID Ukuran tidak ditemukan")
#     else:
#         if int(cek_data["qty_final"]) >= int(cek_data["qty_washing"]):
#             return post_data_fail("Produk tidak tercatat saat pencucian")
#         try:
#             update = update_produk(inv_id)
#             if update:
#                 return success_post_data(True, "Data Berhasil Di Update")
#             return post_data_fail("ID inventory tidak ditemukan")
#         except IntegrityError:
#             return post_data_fail("ID Ukuran tidak ditemukan")


@inv.delete("/del_inv/{id_inv}")
async def delete_data_inventory(id_inv: str):
    try:
        if delete_inv(id_inv):
            return success_post_data(1, "berhasil Menghapus Data")

        return get_data_null("Data Tidak Dapat Di delete")
    except Exception as e:
        get_data_null("Data Tidak Dapat Di delete")
