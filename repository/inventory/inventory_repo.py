import pymysql
from config.database import Db_Mysql, orm_sql
from schemas.inventory import *
from models.inventory.inventori_model import *


def get_all_inventory() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT inventory.id_inv, inventory.id_bahan, inventory.nama_produk, inventory.harga_produk, inventory.qty, inventory.status_trc, bahan.nama_bahan, UPPER(ukuran.nama_ukuran) as ukuran FROM inventory LEFT JOIN ukuran ON ukuran.id_ukuran=inventory.id_ukuran LEFT JOIN bahan ON bahan.id_bahan=inventory.id_bahan"
        cursor.execute(sql)
        return cursor.fetchall()


def get_all_produk_jadi() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT inventory.id_inv, inventory.id_bahan, inventory.nama_produk, inventory.harga_produk, inventory.qty, inventory.status_trc, bahan.nama_bahan, UPPER(ukuran.nama_ukuran) as ukuran FROM inventory LEFT JOIN ukuran ON ukuran.id_ukuran=inventory.id_ukuran LEFT JOIN bahan ON bahan.id_bahan=inventory.id_bahan WHERE status_trc = '3'"
        cursor.execute(sql)
        return cursor.fetchall()


def get_inventory_by_id(id_inventory: str) -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = f"SELECT inventory.id_inv, inventory.id_bahan, inventory.nama_produk, inventory.harga_produk, inventory.qty, inventory.status_trc, bahan.nama_bahan, UPPER(ukuran.nama_ukuran) as ukuran FROM inventory LEFT JOIN ukuran ON ukuran.id_ukuran=inventory.id_ukuran LEFT JOIN bahan ON bahan.id_bahan=inventory.id_bahan WHERE id_inv = '{id_inventory}'"
        cursor.execute(sql)
        return cursor.fetchone()


def create_inventory(inv: InvetoryPostBahan):
    conn = orm_sql()
    data = InventoryMdl(
        id_inv=inv.id_inventory.upper(),
        id_bahan=inv.id_bahan
    )
    conn.add(data)
    conn.commit()
    conn.refresh(data)
    return 1


def update_jahitan(inv: InventoryUpdateProduk, id_inventry: str):
    conn = orm_sql()
    inventory = conn.query(InventoryMdl).filter_by(
        id_inv=id_inventry).first()
    if inventory:
        if inventory.id_ukuran is None:
            inventory.id_ukuran = inv.id_ukuran

        if inventory.harga_produk is None:
            inventory.harga_produk = inv.harga_produk

        if inventory.nama_produk is None:
            inventory.nama_produk = inv.nama_produk

        if inventory.qty is None:
            inventory.qty = 1
        else:
            inventory.qty = int(inventory.qty) + 1
        inventory.status_trc = "1"
        conn.commit()
        return inventory.nama_produk
    return False


def update_cucian(id_inventry: str):
    conn = orm_sql()
    inventory = conn.query(InventoryMdl).filter_by(
        id_inv=id_inventry).first()
    if inventory:
        inventory.status_trc = "2"
        conn.commit()
        return True
    return False


def update_produk(id_inventry: str):
    conn = orm_sql()
    inventory = conn.query(InventoryMdl).filter_by(
        id_inv=id_inventry).first()
    if inventory:
        inventory.status_trc = "3"
        conn.commit()
        return True
    return False


def update_qty_with_pos(qty: int, inv_id: int) -> int:
    conn = orm_sql()
    inv = conn.query(InventoryMdl).filter_by(id_inv=inv_id).first()
    if inv:
        inv.qty = qty
        conn.commit()
        return True
    return False


def delete_inv(inv_id: int) -> int:
    conn = orm_sql()
    data = conn.query(InventoryMdl).filter_by(id_inv=inv_id).first()
    if data:
        conn.delete(data)
        conn.commit()
        return True

    return False
