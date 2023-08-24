import pymysql
from config.database import Db_Mysql, orm_sql
from schemas.ukuran import *
from models.inventory.ukuran_model import *


def get_all_ukuran() -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT UPPER(nama_ukuran) as nama_ukuran, id_ukuran FROM ukuran"
        cursor.execute(sql)
        return cursor.fetchall()


def ukuran_by_id(ukuran_id: str) -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = f"SELECT UPPER(nama_ukuran) as nama_ukuran, id_ukuran FROM ukuran WHERE id_ukuran = '{ukuran_id}'"
        cursor.execute(sql)
        return cursor.fetchone()


def update_ukuran(nama: Ukuran, ukuran_id: int) -> int:
    conn = orm_sql()
    ukuran = conn.query(UkuranMdl).filter_by(id_ukuran=ukuran_id).first()
    if ukuran:
        ukuran.nama_ukuran = nama.nama_ukuran
        conn.commit()
        return True

    return False


def delete_ukuran(ukuran_id: int) -> int:
    conn = orm_sql()
    ukuran = conn.query(UkuranMdl).filter_by(id_ukuran=ukuran_id).first()
    if ukuran:
        conn.delete(ukuran)
        conn.commit()
        return True

    return False


def create_ukuran(ukuran: Ukuran) -> int:
    conn = orm_sql()
    data = UkuranMdl(
        nama_ukuran=ukuran.nama_ukuran.lower()
    )
    conn.add(data)
    conn.commit()
    conn.refresh(data)
    return 1
