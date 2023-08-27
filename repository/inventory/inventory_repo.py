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
        sql = "SELECT inventory.id_inv, inventory.nama_produk, pembuatan.status_pembuatan, inventory.qty_final, DATE_FORMAT(pembuatan.tanggal_pembuatan, '%d-%m-%Y') AS tanggal_pembuatan, DATE_FORMAT(pembuatan.tanggal_selesai, '%d-%m-%Y') AS tanggal_selesai, UPPER(ukuran.nama_ukuran) AS nama_ukuran FROM pembuatan RIGHT JOIN inventory ON inventory.id_inv=pembuatan.id_inv JOIN ukuran ON ukuran.id_ukuran=inventory.id_ukuran"
        cursor.execute(sql)
        return cursor.fetchall()


def get_all_produk_jadi() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT inventory.id_inv, inventory.nama_produk, inventory.qty_final, UPPER(ukuran.nama_ukuran) AS nama_ukuran FROM pembuatan RIGHT JOIN inventory ON inventory.id_inv=pembuatan.id_inv JOIN ukuran ON ukuran.id_ukuran=inventory.id_ukuran  WHERE pembuatan.status_pembuatan='2'"
        cursor.execute(sql)
        return cursor.fetchall()


def get_inventory_by_id(id_inventory: str) -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = f"SELECT inventory.qty_final, inventory.id_inv, inventory.nama_produk, inventory.harga_produk, bahan.nama_bahan, UPPER(ukuran.nama_ukuran) as ukuran FROM inventory LEFT JOIN ukuran ON ukuran.id_ukuran=inventory.id_ukuran LEFT JOIN bahan ON bahan.id_bahan=inventory.id_bahan WHERE id_inv = '{id_inventory}'"
        cursor.execute(sql)
        return cursor.fetchone()


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


def update_jahitan(id_inventry: str):
    conn = orm_sql()
    inventory = conn.query(InventoryMdl).filter_by(
        id_inv=id_inventry).first()
    if inventory:
        if inventory.tanggal_mulai_jait is None:
            inventory.tanggal_mulai_jait = datetime.now()

        if inventory.qty is None:
            inventory.qty = 1
        else:
            inventory.qty = int(inventory.qty) + 1
        inventory.status_trc = "1"
        conn.commit()
        return True
    return False


def update_cucian(id_inventry: str):
    conn = orm_sql()
    inventory = conn.query(InventoryMdl).filter_by(
        id_inv=id_inventry).first()
    if inventory:
        if inventory.qty_final is None:
            inventory.qty_final = 1
        else:
            inventory.qty_final = int(inventory.qty_final) + 1
        conn.commit()
        return True
    return False


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
