import pymysql
from config.database import Db_Mysql, orm_sql
from schemas.bahan import *
from models.inventory.bahan_model import *


def get_all_bahan() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM bahan"
        cursor.execute(sql)
        return cursor.fetchall()


def bahan_by_id(bahan_id: str) -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = f"SELECT * FROM bahan WHERE id_bahan = '{bahan_id}'"
        cursor.execute(sql)
        return cursor.fetchone()


def update_bahan(nama: UpdateBahan, bahan_id: int) -> int:
    conn = orm_sql()
    bahan = conn.query(BahanMdl).filter_by(id_bahan=bahan_id).first()
    if bahan:
        bahan.nama_bahan = nama.nama_bahan
        conn.commit()
        return True
    return False


def delete_bahan(bahan_id: int) -> int:
    conn = orm_sql()
    bahan = conn.query(BahanMdl).filter_by(id_bahan=bahan_id).first()
    if bahan:
        conn.delete(bahan)
        conn.commit()
        return True

    return False


def create_bahan(bahan: Bahan) -> int:
    conn = orm_sql()
    data = BahanMdl(
        id_bahan=bahan.id_bahan,
        nama_bahan=bahan.nama_bahan
    )
    conn.add(data)
    conn.commit()
    conn.refresh(data)
    return 1
