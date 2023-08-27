import pymysql
from config.database import Db_Mysql, orm_sql
from schemas.produksi import *
from repository.inventory.inventory_repo import update_qty_with_pos, get_inventory_by_id
from models.produksi.produksi_model import *


def get_produksi() -> list:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT pembuatan.id_produksi, inventory.nama_produk, pembuatan.status_pembuatan, pembuatan.tanggal_pembuatan, pembuatan.tanggal_selesai, tabel_jait.tanggal_jait, tabel_jait.tanggal_selesai AS selesai_jait, tabel_cuci.tanggal_cuci, tabel_cuci.tanggal_selesai as selesai_cuci, vendor.nama_vendor, vendor.jenis_vendor FROM pembuatan JOIN inventory ON inventory.id_inv=pembuatan.id_inv JOIN tabel_cuci ON tabel_cuci.id_produksi=pembuatan.id_produksi JOIN tabel_jait ON tabel_jait.id_produksi=pembuatan.id_produksi JOIN vendor ON tabel_jait.id_vendor=vendor.id_vendor"
        cursor.execute(query)
        return cursor.fetchall()


def create_produksi(prod: ProduksiScm):
    conn = orm_sql()
    data = PembuatanMdl(
        id_produksi=prod.id_produksi,
        id_inv=prod.id_inv,
        tanggal_pembuatan=prod.tanggal_pembuatan,
        qty_pembuatan=prod.qty_pembuatan,
        status_pembuatan=0
    )
    conn.add(data)
    conn.commit()
    conn.refresh(data)
    return True
