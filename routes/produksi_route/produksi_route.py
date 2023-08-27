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


@produksi.post("/create_prod")
async def post_produksi(prod: ProduksiScm):
    try:
        data_post = create_produksi(prod)
        return data_post
    except IntegrityError:
        return post_data_fail("Data ID Produksi Tidak Ditemukan")
