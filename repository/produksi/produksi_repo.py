import pymysql
import json
from config.database import Db_Mysql, orm_sql
from schemas.produksi import *
from repository.inventory.inventory_repo import update_qty_with_pos, get_inventory_by_id
from models.produksi.produksi_model import *
from models.produksi.jait_model import *
from models.produksi.cuci_model import *
from models.inventory.inventori_model import *


def get_produksi() -> list:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT id_produksi, COUNT(id_inv) AS total_produk, SUM(qty_pembuatan) AS total_quantitas, tanggal_pembuatan, tanggal_selesai, status_pembuatan FROM pembuatan GROUP BY Id_produksi"
        cursor.execute(query)
        results = cursor.fetchall()

        # Convert Decimal values to string
        for result in results:
            result['total_quantitas'] = str(result['total_quantitas'])
            result["tanggal_pembuatan"] = datetime.strftime(
                result["tanggal_pembuatan"], "%d-%m-%Y")

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


def get_produksi_by_id(id_produksi: str) -> list:
    conn = Db_Mysql()
    with conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT
                pembuatan.id_produksi,
                inventory.nama_produk,
                pembuatan.status_pembuatan,
                pembuatan.qty_pembuatan,
                STR_TO_DATE(pembuatan.tanggal_pembuatan, '%d-%m-%Y') AS tanggal_pembuatan,
                STR_TO_DATE(pembuatan.tanggal_selesai, '%d-%m-%Y') AS selesai_pembuatan,
                vendor_jait.nama_vendor AS vendor_jait,
                vendor_cuci.nama_vendor AS vendor_cuci
            FROM pembuatan
            JOIN inventory ON inventory.id_inv = pembuatan.id_inv
            LEFT JOIN tabel_jait ON tabel_jait.id_produksi = pembuatan.id_produksi
            LEFT JOIN tabel_cuci ON tabel_cuci.id_produksi = pembuatan.id_produksi
            LEFT JOIN vendor AS vendor_jait ON vendor_jait.id_vendor = tabel_jait.id_vendor
            LEFT JOIN vendor AS vendor_cuci ON vendor_cuci.id_vendor = tabel_cuci.id_vendor
            WHERE pembuatan.id_produksi = '{}';
        """.format(id_produksi)
        cursor.execute(query)
        return cursor.fetchone()


def create_produksi(prod: ProduksiScm):
    conn = orm_sql()
    date_object = datetime.strptime(prod.tanggal_pembuatan, "%d-%m-%Y")
    data = PembuatanMdl(
        id_produksi=prod.id_produksi,
        id_inv=prod.id_inv,
        tanggal_pembuatan=date_object,
        qty_pembuatan=prod.qty_pembuatan,
        status_pembuatan='0'
    )
    conn.add(data)
    conn.commit()
    conn.refresh(data)
    return True


def create_jaitan(jaitan: CreateJaitan):
    conn = orm_sql()
    data_jaitan = JahitMdl(
        id_produksi=jaitan.id_produksi,
        id_vendor=jaitan.id_vendor,
    )
    conn.add(data_jaitan)
    conn.commit()
    conn.refresh(data_jaitan)
    data_produksi = conn.query(PembuatanMdl).filter_by(
        id_produksi=jaitan.id_produksi.upper()).first()
    if data_produksi:
        data_produksi.status_pembuatan = "1"
        conn.commit()
        return True
    else:
        return False


def create_cucian(cuci: CreateCuci):
    conn = orm_sql()
    # date_object = datetime.strptime(cuci.tanggal_selesai, "%d-%m-%Y")
    data_produksi = conn.query(PembuatanMdl).filter_by(
        id_inv=cuci.id_inv.upper()).first()

    data_inventory = conn.query(InventoryMdl).filter_by(
        id_inv=cuci.id_inv.upper()).first()
    data = CuciMdl(
        id_produksi=cuci.id_produksi,
        id_vendor=cuci.id_vendor
    )
    conn.add(data)
    conn.commit()
    conn.refresh(data)

    if data_produksi:
        data_produksi.tanggal_selesai = datetime.now()
        data_produksi.status_pembuatan = "2"
        data_produksi.status_inventory = "1"
        if data_produksi.qty_inventory is None:
            data_produksi.qty_inventory = 1
        else:
            data_produksi.qty_inventory = int(
                data_produksi.qty_inventory) + 1

        if data_produksi.qty_inventory == data_produksi.qty_pembuatan:
            data_produksi.status_pembuatan = "3"

        if data_inventory:
            if data_inventory.qty_final == 0 or data_inventory.qty_final is None:
                data_inventory.qty_final = 1
            else:
                data_inventory.qty_final = int(data_inventory.qty_final) + 1
        conn.commit()
        return True
    else:
        return False


def updateQtyJaitan(qty_jait: UpdateProduksi, id_inv: str):
    conn = orm_sql()
    data_produksi = conn.query(PembuatanMdl).filter_by(
        id_inv=id_inv.upper()).first()

    if data_produksi:
        data_produksi.qty_pembuatan = qty_jait.qty
        conn.commit()
        return True

    return False
