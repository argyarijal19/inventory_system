import pymysql
import datetime
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from config.database import Db_Mysql, orm_sql
from schemas.inventory import *
from models.inventory.inventori_model import *
from models.inventory.pembuatan_model import *


def get_all_inventory() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT inventory.id_inv, inventory.id_bahan, inventory.id_ukuran, inventory.nama_produk, inventory.harga_produk, inventory.qty_final, UPPER(ukuran.nama_ukuran), bahan.nama_bahan FROM inventory JOIN ukuran ON ukuran.id_ukuran=inventory.id_ukuran JOIN bahan ON bahan.id_bahan=inventory.id_bahan"
        cursor.execute(sql)
        return cursor.fetchall()


def get_all_produk_jadi() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT inventory.id_inv, inventory.nama_produk, inventory.harga_produk, inventory.qty_final, UPPER(ukuran.nama_ukuran) AS nama_ukuran FROM pembuatan RIGHT JOIN inventory ON inventory.id_inv=pembuatan.id_inv JOIN ukuran ON ukuran.id_ukuran=inventory.id_ukuran  WHERE pembuatan.status_inventory='1' GROUP BY id_inv"
        cursor.execute(sql)
        return cursor.fetchall()


def get_inventory_by_id(id_inventory: str) -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = f"SELECT inventory.qty_final, inventory.id_inv, inventory.nama_produk, inventory.harga_produk, bahan.nama_bahan, UPPER(ukuran.nama_ukuran) as ukuran FROM inventory LEFT JOIN ukuran ON ukuran.id_ukuran=inventory.id_ukuran LEFT JOIN bahan ON bahan.id_bahan=inventory.id_bahan WHERE id_inv = '{id_inventory}'"
        cursor.execute(sql)
        return cursor.fetchone()


def get_barang_cucian():
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = """
            SELECT p1.id_produksi,
                SUM(p1.qty_pembuatan) + COALESCE(p2.total_quantitas_after, 0) AS total_quantitas,
                COALESCE(p1.qty_inventory, 0) + COALESCE(p2.total_selesai_cuci_after, 0) AS total_selesai_cuci,
                p1.tanggal_pembuatan,
                p1.tanggal_selesai,
                p1.status_pembuatan,
                        COUNT(p1.id_inv) + COALESCE(p2.total_produk_selesai, 0) AS total_produk_cuci,
                COALESCE(p2.total_produk_selesai, 0) AS total_produk_selesai
            FROM pembuatan p1
            LEFT JOIN (
                SELECT id_produksi, COUNT(id_inv) AS total_produk_selesai, SUM(qty_pembuatan) AS total_quantitas_after, SUM(CASE WHEN status_pembuatan = '3' THEN qty_inventory ELSE 0 END) AS total_selesai_cuci_after
                FROM pembuatan
                WHERE status_pembuatan = '3'
                GROUP BY id_produksi
            ) p2 ON p1.id_produksi = p2.id_produksi
            WHERE p1.status_pembuatan = '2'
            GROUP BY p1.id_produksi, p1.tanggal_pembuatan, p1.tanggal_selesai, p1.status_pembuatan;
       """
        cursor.execute(sql)
        results = cursor.fetchall()

        # Convert Decimal values to string
        for result in results:
            result['total_quantitas'] = int(result['total_quantitas'])
            result["tanggal_pembuatan"] = datetime.strftime(
                result["tanggal_pembuatan"], "%d-%m-%Y")
            result['total_selesai_cuci'] = int(result['total_selesai_cuci'])

            if result["tanggal_selesai"] is not None:
                result["tanggal_selesai"] = datetime.strftime(
                    result["tanggal_selesai"], "%d-%m-%Y")
            else:
                result["tanggal_selesai"] = None

        return results


def get_cucian_by_id(produksi_id: str) -> list:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT
                inventory.id_inv,
                pembuatan.id_produksi,
                inventory.nama_produk,
                pembuatan.status_pembuatan,
                pembuatan.qty_pembuatan,
                UPPER(ukuran.nama_ukuran) AS nama_ukuran,
                DATE(pembuatan.tanggal_pembuatan) AS tanggal_pembuatan,
                DATE(pembuatan.tanggal_selesai) AS selesai_pembuatan,
                vendor_jait.nama_vendor AS vendor_jait,
                vendor_cuci.nama_vendor AS vendor_cuci
            FROM pembuatan
            JOIN inventory ON inventory.id_inv = pembuatan.id_inv
            LEFT JOIN ukuran ON inventory.id_ukuran = ukuran.id_ukuran
            LEFT JOIN tabel_jait ON tabel_jait.id_produksi = pembuatan.id_produksi
            LEFT JOIN tabel_cuci ON tabel_cuci.id_produksi = pembuatan.id_produksi
            LEFT JOIN vendor AS vendor_jait ON vendor_jait.id_vendor = tabel_jait.id_vendor
            LEFT JOIN vendor AS vendor_cuci ON vendor_cuci.id_vendor = tabel_cuci.id_vendor
            WHERE pembuatan.id_produksi = '{}';
        """.format(produksi_id)
        cursor.execute(query)
        results = cursor.fetchall()

        for result in results:
            result["tanggal_pembuatan"] = datetime.strftime(
                result["tanggal_pembuatan"], "%d-%m-%Y")

            if result["selesai_pembuatan"] is not None:
                result["selesai_pembuatan"] = datetime.strftime(
                    result["selesai_pembuatan"], "%d-%m-%Y")

        return results


def get_barang_jaitan():
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT id_produksi, COUNT(id_inv) AS total_produk, SUM(qty_pembuatan) AS total_quantitas, SUM(qty_inventory) AS total_selesai_cuci, tanggal_pembuatan, tanggal_selesai, status_pembuatan FROM pembuatan WHERE status_pembuatan = '1' GROUP BY Id_produksi"
        cursor.execute(sql)
        results = cursor.fetchall()

        # Convert Decimal values to string
        for result in results:
            result['total_quantitas'] = str(result['total_quantitas'])
            result["tanggal_pembuatan"] = datetime.strftime(
                result["tanggal_pembuatan"], "%d-%m-%Y")
            result['total_selesai_cuci'] = str(result['total_selesai_cuci'])

            if result["tanggal_selesai"] is not None:
                result["tanggal_selesai"] = datetime.strftime(
                    result["tanggal_selesai"], "%d-%m-%Y")
            else:
                result["tanggal_selesai"] = None

        return results


def get_jaitan_by_id(produksi_id: str) -> list:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT
                inventory.id_inv,
                pembuatan.id_produksi,
                inventory.nama_produk,
                pembuatan.status_pembuatan,
                pembuatan.qty_pembuatan,
                UPPER(ukuran.nama_ukuran) AS nama_ukuran,
                STR_TO_DATE(pembuatan.tanggal_pembuatan, '%d-%m-%Y') AS tanggal_pembuatan,
                STR_TO_DATE(pembuatan.tanggal_selesai, '%d-%m-%Y') AS selesai_pembuatan,
                vendor_jait.nama_vendor AS vendor_jait,
                vendor_cuci.nama_vendor AS vendor_cuci
            FROM pembuatan
            JOIN inventory ON inventory.id_inv = pembuatan.id_inv
            LEFT JOIN ukuran ON inventory.id_ukuran = ukuran.id_ukuran
            LEFT JOIN tabel_jait ON tabel_jait.id_produksi = pembuatan.id_produksi
            LEFT JOIN tabel_cuci ON tabel_cuci.id_produksi = pembuatan.id_produksi
            LEFT JOIN vendor AS vendor_jait ON vendor_jait.id_vendor = tabel_jait.id_vendor
            LEFT JOIN vendor AS vendor_cuci ON vendor_cuci.id_vendor = tabel_cuci.id_vendor
            WHERE pembuatan.id_produksi = '{}' AND pembuatan.status_pembuatan = '1';
        """.format(produksi_id)
        cursor.execute(query)
        return cursor.fetchall()


def create_inventory(inv: InvetoryPostBahan):
    conn = orm_sql()
    inventory = conn.query(InventoryMdl).filter_by(
        id_inv=inv.id_inventory.upper()).first()
    data = InventoryMdl(
        id_inv=inv.id_inventory.upper(),
        id_bahan=inv.id_bahan,
        id_ukuran=inv.id_ukuran,
        nama_produk=inv.nama_produk,
        harga_produk=inv.harga_produk,
    )
    conn.add(data)
    conn.commit()
    conn.refresh(data)
    return True


def create_pembuatan(id_inv, qty):
    conn = orm_sql()
    pembuatan = conn.query(func.max(PembuatanMdl.interval_pembuatan)).filter_by(
        id_inv=id_inv).scalar()
    records_with_max_interval = conn.query(PembuatanMdl).filter_by(
        id_inv=id_inv, interval_pembuatan=pembuatan).first()
    if records_with_max_interval:
        data = PembuatanMdl(
            id_inv=id_inv,
            qty_pembuatan=qty,
            tanggal_pembuatan=datetime.now(),
            interval_pembuatan=pembuatan + 1,
        )
    else:
        data = PembuatanMdl(
            id_inv=id_inv,
            qty_pembuatan=qty,
            tanggal_pembuatan=datetime.now(),
            interval_pembuatan=1,
        )
    conn.add(data)
    conn.commit()
    conn.refresh(data)
    return True


def update_pembuatan(inv_id: str, qty: int):
    conn = orm_sql()
    max_interval = conn.query(func.max(PembuatanMdl.interval_pembuatan)).filter_by(
        id_inv=inv_id).scalar()
    if max_interval:
        records_with_max_interval = conn.query(PembuatanMdl).filter_by(
            id_inv=inv_id, interval_pembuatan=max_interval).first()
        if records_with_max_interval:
            records_with_max_interval.tanggal_selesai = datetime.now()
            records_with_max_interval.qty_pembuatan = qty
            conn.commit()
            return True


# def update_jahitan(id_inventry: str):
#     conn = orm_sql()
#     inventory = conn.query(InventoryMdl).filter_by(
#         id_inv=id_inventry).first()
#     if inventory:
#         if inventory.tanggal_mulai_jait is None:
#             inventory.tanggal_mulai_jait = datetime.now()

#         if inventory.qty is None:
#             inventory.qty = 1
#         else:
#             inventory.qty = int(inventory.qty) + 1
#         inventory.status_trc = "1"
#         conn.commit()
#         return True
#     return False


# def update_cucian(id_inventry: str):
#     conn = orm_sql()
#     inventory = conn.query(InventoryMdl).filter_by(
#         id_inv=id_inventry).first()
#     if inventory:
#         if inventory.qty_final is None:
#             inventory.qty_final = 1
#         else:
#             inventory.qty_final = int(inventory.qty_final) + 1
#         conn.commit()
#         return True
#     return False


def update_inventory(prod: UpdateInventory, id_inventory: int):
    conn = orm_sql()
    data_exist = conn.query(InventoryMdl).filter_by(
        id_inv=id_inventory).first()

    if data_exist:
        data_exist.harga_produk = prod.harga_produk
        data_exist.nama_produk = prod.nama_produk
        conn.commit()
        return True

# def update_produk(id_inventry: str, status_trc: str):
#     conn = orm_sql()
#     inventory = conn.query(InventoryMdl).filter_by(
#         id_inv=id_inventry).first()
#     if inventory:
#         if inventory.qty_final is None:
#             inventory.qty_final = 1
#         else:
#             inventory.qty_final = int(inventory.qty_washing) + 1
#         inventory.tanggal_produk_jadi = datetime.now()
#         inventory.status_trc = status_trc
#         conn.commit()
#         return True
#     return False


def update_qty_with_pos(qty: int, inv_id: int) -> int:
    conn = orm_sql()
    inv = conn.query(InventoryMdl).filter_by(id_inv=inv_id).first()
    if inv:
        inv.qty_final = qty
        conn.commit()
        return True
    return False


def delete_inv(inv_id: int) -> int:
    conn = orm_sql()
    data = conn.query(InventoryMdl).filter_by(id_inv=inv_id).first()
    if data:
        try:
            conn.delete(data)
            conn.commit()
            return True
        except IntegrityError:
            return False
    else:
        return False
