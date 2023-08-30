import pymysql
import json
from sqlalchemy import update
from config.database import Db_Mysql, orm_sql
from schemas.produksi import *
from models.produksi.produksi_model import *
from models.produksi.jait_model import *
from models.produksi.cuci_model import *
from models.inventory.inventori_model import *


def get_produksi() -> list:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT id_produksi, COUNT(id_inv) AS total_produk, SUM(qty_pembuatan) AS total_quantitas,  SUM(qty_inventory) AS total_quantitas_sudah_digudang, tanggal_pembuatan, tanggal_selesai, status_pembuatan FROM pembuatan GROUP BY Id_produksi"
        cursor.execute(query)
        results = cursor.fetchall()

        # Convert Decimal values to string
        for result in results:
            result['total_quantitas'] = int(result['total_quantitas'])
            result["tanggal_pembuatan"] = datetime.strftime(
                result["tanggal_pembuatan"], "%d-%m-%Y")
            if result["total_quantitas_sudah_digudang"] is None:
                result["total_quantitas_sudah_digudang"] = None
            else:
                result["total_quantitas_sudah_digudang"] = int(
                    result["total_quantitas_sudah_digudang"])
            if result["tanggal_selesai"] is not None:
                result["tanggal_selesai"] = datetime.strftime(
                    result["tanggal_selesai"], "%d-%m-%Y")
            else:
                result["tanggal_selesai"] = None

        return results


def get_id_for_qrcode(id_produksi: str):
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = f"SELECT id_produksi, COUNT(id_inv) AS total_produk, SUM(qty_pembuatan) AS total_quantitas, tanggal_pembuatan, tanggal_selesai, status_pembuatan FROM pembuatan WHERE id_produksi = '{id_produksi}' GROUP BY Id_produksi "
        cursor.execute(sql)
        return cursor.fetchone()


def get_status_pebuatan(id_inv: str) -> dict:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = f"SELECT id_produksi, status_pembuatan FROM pembuatan WHERE id_inv = '{id_inv}' AND status_pembuatan = '2'"
        cursor.execute(sql)
        return cursor.fetchone()


def get_produksi_by_id(id_produksi: str) -> list:
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
            WHERE pembuatan.id_produksi = '{}';
        """.format(id_produksi)
        cursor.execute(query)
        return cursor.fetchall()


def create_produksi(prod: ProduksiScm):
    conn = orm_sql()

    date_object = datetime.strptime(prod.tanggal_pembuatan, "%d-%m-%Y")
    data_jahitan = conn.query(JahitMdl).filter_by(
        id_produksi=prod.id_produksi).first()

    data_produksi = conn.query(PembuatanMdl).filter_by(
        id_produksi=prod.id_produksi, id_inv=prod.id_inv).first()

    if data_produksi is None:
        data = PembuatanMdl(
            id_produksi=prod.id_produksi,
            id_inv=prod.id_inv,
            tanggal_pembuatan=date_object,
            qty_pembuatan=prod.qty_pembuatan,
            status_pembuatan='1'
        )
        conn.add(data)
        conn.commit()
        conn.refresh(data)
    else:
        data_produksi.qty_pembuatan = int(
            data_produksi.qty_pembuatan) + prod.qty_pembuatan
        conn.commit()

    if data_jahitan is None:
        data_jaitan = JahitMdl(
            id_produksi=prod.id_produksi,
            id_vendor=prod.id_vendor,
        )
        conn.add(data_jaitan)
        conn.commit()
        conn.refresh(data_jaitan)
    return True


# def create_jaitan(jaitan: CreateJaitan):
#     conn = orm_sql()
#     data_jaitan = JahitMdl(
#         id_produksi=jaitan.id_produksi,
#         id_vendor=jaitan.id_vendor,
#     )
#     conn.add(data_jaitan)
#     conn.commit()
#     conn.refresh(data_jaitan)
#     data_produksi = conn.query(PembuatanMdl).filter_by(
#         id_produksi=jaitan.id_produksi.upper()).first()
#     if data_produksi:
#         data_produksi.status_pembuatan = "1"
#         conn.commit()
#         return True
#     else:
#         return False

def create_inventory(inv: CreateInventory):
    conn = orm_sql()
    data_pembuatan = conn.query(PembuatanMdl).filter_by(
        id_inv=inv.id_inv, status_pembuatan="2").first()

    data_inventory = conn.query(InventoryMdl).filter_by(
        id_inv=inv.id_inv.upper()).first()

    if data_inventory and data_pembuatan:
        data_pembuatan.status_inventory = "1"
        if data_inventory.qty_final == 0 or data_inventory.qty_final is None:
            data_inventory.qty_final = 1
        else:
            data_inventory.qty_final = int(
                data_inventory.qty_final) + 1

        if data_pembuatan.qty_inventory is not None:
            data_pembuatan.qty_inventory = int(
                data_pembuatan.qty_inventory) + 1
            if data_pembuatan.qty_inventory == data_pembuatan.qty_pembuatan:
                data_pembuatan.status_pembuatan = "3"
                data_pembuatan.tanggal_selesai = datetime.now().date()

        else:
            data_pembuatan.qty_inventory = 1

        conn.commit()
        return data_pembuatan

    return False


def create_cucian(cuci: CreateCuci):
    conn = orm_sql()

    data_produksi = conn.query(PembuatanMdl).filter(
        PembuatanMdl.id_produksi == cuci.id_produksi.upper()).all()

    data_cuci = conn.query(CuciMdl).filter_by(
        id_produksi=cuci.id_produksi.upper()).first()

    if data_cuci is None:
        data = CuciMdl(
            id_produksi=cuci.id_produksi,
            id_vendor=cuci.id_vendor
        )
        conn.add(data)
        conn.commit()
        conn.refresh(data)

    if data_produksi:
        stmt = update(PembuatanMdl).where(PembuatanMdl.id_produksi ==
                                          cuci.id_produksi).values(status_pembuatan="2")
        conn.execute(stmt)
        conn.commit()
        return True
    else:
        return False


def updateQtyJaitan(qty_jait: UpdateProduksi, id_inv: str):
    conn = orm_sql()
    data_produksi = conn.query(PembuatanMdl).filter_by(
        id_inv=id_inv.upper(), id_produksi=qty_jait.id_produksi).first()

    if data_produksi:
        data_produksi.qty_pembuatan = qty_jait.qty
        conn.commit()
        return True

    return False
