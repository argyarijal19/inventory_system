from fastapi import APIRouter
from repository.pos.po_repo import *
from repository.inventory.inventory_repo import get_inventory_by_id, update_qty_with_pos
from sqlalchemy.exc import IntegrityError
from helper.response import *
from helper.make_qrcode import Generate_qrcode
from schemas.pos import *

pos = APIRouter(prefix="/pos", tags=["Point Of Sale Detail"])


@pos.get("/")
async def get_data_pos_all():
    data = get_all_pos()
    if data:
        return success_get_data(data)
    return get_data_null("data Point Of Sale tidak ditemukan")


@pos.get("/{id_pos}")
async def get_data_pos_by_id(id_pos: int):
    data = get_pos_by_id(id_pos)
    if data:
        return success_get_data(data)
    return get_data_null("data Point Of Sale tidak ditemukan")


@pos.get("/pendapatan_bulan_ini/")
async def summary_pendapatan_bulan_ini():
    data = penjualan_bulan_ini()
    cost = cost_bulan_ini()
    if data:
        data_penjualan_hari_ini = {}
        if cost["percentage_change"] is not None:
            data_penjualan_hari_ini["cost_bulan_ini"] = float("{:.2f}".format(cost["percentage_change"]))
            data_penjualan_hari_ini["pendapatan_bulan_ini"] = float(
                data["total_penjualan"])
        else:
            data_penjualan_hari_ini["cost_bulan_ini"] = float(0.0)
            data_penjualan_hari_ini["pendapatan_bulan_ini"] = float(
                data["total_penjualan"])
        return success_get_data(data_penjualan_hari_ini)
    return get_data_null("Penjualan Bulan ini Belum")


@pos.get("/pendapatan_hari_ini/")
async def summary_pendapatan_hari_ini():
    data = penjualan_hari_ini()
    cost = cost_hari_ini()
    if data:
        data_penjualan_hari_ini = {}
        if cost["percentage_change"] is not None:
            data_penjualan_hari_ini["cost_hari_ini"] = float("{:.2f}".format(cost["percentage_change"]))
            data_penjualan_hari_ini["pendapatan_hari_ini"] = float(
                data["total_penjualan"])
        else:
            data_penjualan_hari_ini["cost_hari_ini"] = int(0)
            data_penjualan_hari_ini["pendapatan_hari_ini"] = float(
                data["total_penjualan"])
        return success_get_data(data_penjualan_hari_ini)
    return get_data_null("Penjualan Bulan ini Belum")


@pos.get("/total_penjualan/")
async def summary_total_penjualan():
    data = total_penjualan()
    if data:
        total = int(data["total_produk_terjual"])
        return success_get_data({"total_penjualan": total})
    return get_data_null("Penjualan Bulan ini Belum")


@pos.get("/total_pendapatan/")
async def summary_total_pendapatan():
    data = total_keuntungan()
    if data:
        total = int(data["total_keuntungan"])
        return success_get_data({"total_penjualan": total})
    return get_data_null("Penjualan Bulan ini Belum")


@pos.get("/total_penjualan_per_bulan/")
async def summary_total_penjualan_per_bulan():
    data = total_penjualan_per_bulan()
    if data:
        for entry in data:
            entry["total_produk_terjual"] = float(
                entry["total_produk_terjual"])
            entry["total_keuntungan"] = float(entry["total_keuntungan"])
        return success_get_data(data)
    return get_data_null("Penjualan Bulan ini Belum")


@pos.post("/create_pos")
async def create_pos_data(pos: Pos):
    data_inv = get_inventory_by_id(pos.id_inv)
    if data_inv:
        total_income = pos.total_qty * data_inv["harga_produk"]
        result_qty = data_inv["qty_final"] - pos.total_qty
        if result_qty < 0:
            nama_produk = data_inv["nama_produk"]
            id_produk = data_inv["id_inv"]
            stok_produk = data_inv["qty_final"]
            return post_data_fail(f"produk {nama_produk} dengan id {id_produk} hanya memiliki stok sebanyak {stok_produk}, Quantity yang di inpukan melebihi stock nya")

        update_qty = update_qty_with_pos(result_qty, pos.id_inv)
        if update_qty:
            try:
                create_data = create_pos(pos, total_income)
                if create_data:
                    return success_post_data(create_data, "berhasil create data point of sale")
            except IntegrityError:
                return post_data_fail("Gagal create data point of sale")

    return post_data_fail("Gagal create data point of sale,  ID inventory tidak sesuai")
