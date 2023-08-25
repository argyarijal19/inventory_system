import pymysql
from config.database import Db_Mysql, orm_sql
from schemas.pos import *
from repository.inventory.inventory_repo import update_qty_with_pos, get_inventory_by_id
from models.pos.pos_model import *


def get_all_pos() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT pos.id_pos, pos.id_inv, pos.total_qty, pos.total_income, inventory.nama_produk, inventory.harga_produk FROM pos JOIN inventory ON inventory.id_inv=pos.id_inv"
        cursor.execute(sql)
        return cursor.fetchall()


def get_pos_by_id(id_pos: int) -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = f"SELECT pos.id_pos, pos.id_inv, pos.total_qty, pos.total_income, inventory.nama_produk, inventory.harga_produk FROM pos JOIN inventory ON inventory.id_inv=pos.id_inv WHERE id_pos = {id_pos}"
        cursor.execute(sql)
        return cursor.fetchone()


def penjualan_bulan_ini() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT SUM(total_income) AS total_penjualan FROM pos WHERE tanggal_barang_out >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY);"
        cursor.execute(sql)
        return cursor.fetchall()[0]


def penjualan_hari_ini() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT SUM(total_income) AS total_penjualan FROM pos WHERE tanggal_barang_out >= DATE_SUB(CURRENT_DATE, INTERVAL 1 DAY);"
        cursor.execute(sql)
        return cursor.fetchall()[0]


def total_penjualan() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT SUM(total_qty) AS total_produk_terjual FROM pos;"
        cursor.execute(sql)
        return cursor.fetchall()[0]


def total_keuntungan() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT SUM(total_income) AS total_keuntungan FROM pos"
        cursor.execute(sql)
        return cursor.fetchall()[0]


def total_penjualan_per_bulan() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = """
        SELECT 
            YEAR(tanggal_barang_out) AS tahun, 
            MONTH(tanggal_barang_out) AS bulan, 
            SUM(total_qty) AS total_produk_terjual,
            SUM(total_income) AS total_keuntungan
        FROM pos
            GROUP BY YEAR(tanggal_barang_out), MONTH(tanggal_barang_out)
            ORDER BY tahun, bulan;
        """
        cursor.execute(sql)
        return cursor.fetchall()


def create_pos(pos: Pos, total_income: int) -> int:
    conn = orm_sql()
    data = PosMdl(
        id_inv=pos.id_inv,
        total_qty=pos.total_qty,
        total_income=total_income
    )
    conn.add(data)
    conn.commit()
    conn.refresh(data)
    return 1
