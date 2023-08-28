import pymysql
from config.database import Db_Mysql, orm_sql
from schemas.produksi import CreateVendor
from models.produksi.vendor_model import VendorMdl


def get_vendor() -> list:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT id_vendor, nama_vendor, jenis_vendor FROM vendor"
        cursor.execute(query)
        return cursor.fetchall()


def get_vendor_by_id(id_vendor: int) -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = f"SELECT id_vendor, nama_vendor, jenis_vendor FROM vendor WHERE id_vendor = '{id_vendor}'"
        cursor.execute(query)
        return cursor.fetchone()


def create_vendor(ven: CreateVendor):
    conn = orm_sql()
    data = VendorMdl(
        nama_vendor=ven.nama_vendor,
        jenis_vendor=ven.jenis_vendor
    )
    conn.add(data)
    conn.commit()
    conn.refresh(data)
    return True


def update_vendor(ven: CreateVendor, vendor_id: int):
    conn = orm_sql()
    data_vendor = conn.query(VendorMdl).filter_by(id_vendor=vendor_id).first()
    if data_vendor:
        data_vendor.nama_vendor = ven.nama_vendor
        data_vendor.jenis_vendor = ven.jenis_vendor
        conn.commit()
        return True


def delete_vendor(vendor_id: int):
    conn = orm_sql()
    data_vendor = conn.query(VendorMdl).filter_by(id_vendor=vendor_id).first()
    if data_vendor:
        conn.delete(data_vendor)
        conn.commit()
        return True

    return False
