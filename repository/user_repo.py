import pymysql
import hashlib
import bcrypt
from config.database import Db_Mysql, orm_sql
from schemas.user import *
from models.user_model import UserMdl


def hash_password(password):
    # Generate salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def check_password(password, hashed_password):
    # Check if the provided password matches the hashed password
    string_encode = password.encode('utf-8')
    check = bcrypt.checkpw(string_encode, hashed_password)
    return check


def generate_unique_id(username, full_name):
    # Menggabungkan username dan nama lengkap
    combined_string = username + full_name

    # Menggunakan hash SHA-256
    sha256_hash = hashlib.sha256(combined_string.encode()).hexdigest()

    # Mengambil 20 karakter pertama dari hash
    unique_id = sha256_hash[:20]

    return unique_id


def create_user(user: Register) -> bool:
    conn = orm_sql()
    hashID = generate_unique_id(user.username, user.nama_lengkap)
    hashPW = hash_password(user.password)

    data = UserMdl(
        id_user=hashID,
        username=user.username,
        nama_lengkap=user.nama_lengkap,
        password=hashPW
    )
    conn.add(data)
    conn.commit()
    conn.refresh(data)
    return True


def login(user: Login) -> dict:
    conn = orm_sql()
    data_user = conn.query(UserMdl).filter_by(username=user.username).first()
    results = {}
    if data_user:
        verify_pass = check_password(
            user.password, data_user.password.encode('utf-8'))
        if verify_pass:
            results = {
                "message": None,
                "username": data_user.username,
                "nama_lengkap": data_user.nama_lengkap,
                "id_user": data_user.id_user
            }
            return results
        else:
            results = {
                "message": "Password Tidak Valid"
            }
            return results
    else:
        results = {
            "message": "Username Tidak Valid"
        }
        return results
