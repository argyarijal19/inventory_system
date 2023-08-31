import pymysql
from config.database import Db_Mysql, orm_sql
from schemas.pos import *
from repository.inventory.inventory_repo import update_qty_with_pos, get_inventory_by_id
from models.pos.pos_model import *


def get_all_pos() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT COUNT(pos.id_pos) AS total_penjualan, pos.id_inv, SUM(pos.total_qty) AS total_qty, SUM(pos.total_income) AS total_income, inventory.nama_produk, inventory.harga_produk FROM pos JOIN inventory ON inventory.id_inv=pos.id_inv GROUP BY pos.id_inv"
        cursor.execute(sql)
        results = cursor.fetchall()

        for result in results:
            if result["total_penjualan"] is not None:
                result["total_penjualan"] = int(result["total_penjualan"])

            if result["total_qty"] is not None:
                result["total_qty"] = int(result["total_qty"])

            if result["total_income"] is not None:
                result["total_income"] = int(result["total_income"])

        return results


def get_pos_by_id(id_inv: int) -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = f"SELECT pos.id_pos, pos.id_inv, CONVERT(SUM(pos.total_qty), SIGNED) AS total_qty, CONVERT(SUM(pos.total_income), SIGNED) AS total_income, inventory.nama_produk, DATE_FORMAT(pos.tanggal_barang_out, '%d-%m-%Y') AS tanggal_barang_out, inventory.harga_produk FROM pos JOIN inventory ON inventory.id_inv=pos.id_inv WHERE pos.id_inv = '{id_inv}' GROUP BY tanggal_barang_out"
        cursor.execute(sql)
        results = cursor.fetchall()

        return results


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
        sql = "SELECT SUM(total_income) AS total_penjualan FROM pos WHERE DATE(tanggal_barang_out) = CURDATE();"
        cursor.execute(sql)
        return cursor.fetchone()


def cost_hari_ini():
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            SELECT 
                LEAST(GREATEST(((total_income_today - total_income_yesterday) / total_income_today) * 100, -100), 100) AS percentage_change  
            FROM (
                SELECT 
                    (SELECT SUM(total_income) FROM pos WHERE DATE(tanggal_barang_out) = CURDATE()) AS total_income_today,
                    (SELECT SUM(total_income) FROM pos WHERE DATE(tanggal_barang_out) = CURDATE() - INTERVAL 1 DAY) AS total_income_yesterday
            ) AS income_comparison;
        """
        cursor.execute(sql)
        return cursor.fetchone()


def cost_bulan_ini():
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            SELECT 
                LEAST(GREATEST(((total_income_today - total_income_yesterday) / total_income_today) * 100, -100), 100) AS percentage_change  
            FROM (
                SELECT 
                    (SELECT SUM(total_income) FROM pos WHERE DATE_FORMAT(tanggal_barang_out, '%Y-%m') = DATE_FORMAT(CURDATE(), '%Y-%m')) AS total_income_today,
                    (SELECT SUM(total_income) FROM pos WHERE DATE_FORMAT(tanggal_barang_out, '%Y-%m') = DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m'))AS total_income_yesterday
            ) A
        """
        cursor.execute(sql)
        return cursor.fetchone()


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
        total_qty=1,
        total_income=total_income
    )
    conn.add(data)
    conn.commit()
    conn.refresh(data)
    return 1
