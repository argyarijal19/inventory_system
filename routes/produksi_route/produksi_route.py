from fastapi import APIRouter
from repository.produksi.produksi_repo import *
from repository.inventory.inventory_repo import get_inventory_by_id, update_qty_with_pos
from sqlalchemy.exc import IntegrityError
from helper.response import *
from helper.make_qrcode import Generate_qrcode
from schemas.produksi import *

produksi = APIRouter(prefix="/produksi", tags=["Produksi Detail"])


@produksi.get("/")
async def produksi_all_data():
    data = get_produksi()
    if data:
        return success_get_data(data)
    return get_data_null("Data Produksi Belum Ada")


@produksi.get("/qrcode/{id_produksi}")
async def produksi_all_data(id_produksi: str):
    data = get_id_for_qrcode(id_produksi)
    if data:
        qrcode = Generate_qrcode(data["id_produksi"])
        if data["tanggal_selesai"] is not None:
            data_response = {
                "id_produksi": data["id_produksi"],
                "qty_pembuatan": int(data["total_quantitas"]),
                "total_produk_dibuat": int(data["total_produk"]),
                "tanggal_pembuatan": datetime.strftime(data["tanggal_pembuatan"], "%d-%m-%Y"),
                "tanggal_selesai": datetime.strftime(data["tanggal_selesai"], "%d-%m-%Y"),
                "status_pembuatan": int(data["status_pembuatan"]),
                "qr_code": qrcode
            }
        else:
            data_response = {
                "id_produksi": data["id_produksi"],
                "qty_pembuatan": int(data["total_quantitas"]),
                "total_produk_dibuat": int(data["total_produk"]),
                "tanggal_pembuatan": datetime.strftime(data["tanggal_pembuatan"], "%d-%m-%Y"),
                "tanggal_selesai": None,
                "status_pembuatan": int(data["status_pembuatan"]),
                "qr_code": qrcode
            }
        return success_get_data(data_response)
    return get_data_null("Data Produksi Belum Ada")


@produksi.get("/{id_produksi}")
async def get_data_produksi_by_id(id_produksi: str):
    dataProduksi = get_produksi_by_id(id_produksi)
    if dataProduksi:
        return success_get_data(dataProduksi)

    return get_data_null(f"Data Produksi Dengan ID {id_produksi} Tidak di temukan")


# @produksi.post("/post_jaitan")
# async def post_jaitan_produksi(jait: CreateJaitan):
#     try:
#         post_jaitan = create_jaitan(jait)
#         if post_jaitan:
#             return success_post_data(1, "Berhasil Menambahkan Jaitan")

#         return post_data_fail("Gagal Menambahkan jaitan")
#     except IntegrityError:
#         return post_data_fail("ID Vendor tidak ditemukan")


@produksi.put("/update_qty_after_jait/{id_inv}")
async def put_qty_after_jait(update_qty: UpdateProduksi, id_inv: str):
    update = updateQtyJaitan(update_qty, id_inv)
    if update:
        return success_post_data(1, "Update Data Berhasil")

    return post_data_fail("Data Gagal DI update")


@produksi.put("/update_inventory/")
async def update_inventory(inv: CreateInventory):
    try:
        create_data = create_inventory(inv)
        if create_data:
            return success_post_data(1, "Produk Berhasil Masuk Ke gudang")
        else:
            return post_data_fail("total kuantitas yang di buat kurang dari total kuantitas yang ingin ditambahkan ke gudang")
    except:
        return post_data_fail("data gagal ditambahkan")


@produksi.post("/create_prod")
async def post_produksi(prod: ProduksiScm):
    try:
        data_post = create_produksi(prod)
        return data_post
    except IntegrityError:
        return post_data_fail("Data ID Produk Tidak Ditemukan")


@produksi.put("/create_cucian")
async def update_data_cuci(cucian: CreateCuci):
    data_produksi = get_produksi_by_id(cucian.id_produksi)
    if data_produksi:
        status_pem = data_produksi[0]["status_pembuatan"]
        if status_pem == "1":
            try:
                update_data = create_cucian(cucian)
                if update_data:
                    return success_post_data(1, "Berhasil Update Data")

                return success_post_data(1, "Berhasil Update Cucian")
            except IntegrityError:
                return post_data_fail("Data Vendor Tidak Ditemukan")
        else:
            return post_data_fail("Produksi Ini belum Melalui Tahap Penjahitan")
    else:
        return post_data_fail("ID Produksi Tidak Ditemukan")
