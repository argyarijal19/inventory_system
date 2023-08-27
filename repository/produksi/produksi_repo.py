import pymysql
from config.database import Db_Mysql, orm_sql
from schemas.produksi import *
from repository.inventory.inventory_repo import update_qty_with_pos, get_inventory_by_id
from models.produksi.produksi_model import *


def get_produksi() -> list:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT inventory.nama_produk, pembuatan.status_pembuatan, pembuatan.status_pembuatan, pembuatan.tanggal_pembuatan, pembuatan.tanggal_selesai, vendor.nama_vendor, vendor.jenis_vendor FROM pembuatan JOIN inventory ON inventory.id_inv=pembuatan.id_inv LEFT JOIN vendor ON vendor.id_vendor=pembuatan.id_vendor"
        cursor.execute(query)
        return cursor.fetchall()
