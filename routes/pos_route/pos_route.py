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


@pos.post("/create_pos")
async def create_pos_data(pos: Pos):
    data_inv = get_inventory_by_id(pos.id_inv)
    if data_inv:
        total_income = pos.total_qty * data_inv["harga_produk"]
        result_qty = data_inv["qty"] - pos.total_qty
        if result_qty < 0:
            return post_data_fail("total Quantity melebihi stock nya")

        update_qty = update_qty_with_pos(result_qty, pos.id_inv)
        if update_qty:
            try:
                create_data = create_pos(pos, total_income)
                if create_data:
                    return success_post_data(create_data, "berhasil create data point of sale")
            except IntegrityError:
                return post_data_fail("Gagal create data point of sale")

    return post_data_fail("Gagal create data point of sale,  ID inventory tidak sesuai")
