import re
from fastapi import APIRouter
from schemas.user import *
from repository.user_repo import *
from helper.response import *

auth = APIRouter(prefix="/user", tags=["AUYHENTICATION Detail"])


@auth.post("/register/")
async def register_user(user: Register):
    role_username = r"^(?=.*\d.*\d)[a-zA-Z0-9]{6,15}$"
    role_password = r"^(?=.*[A-Za-z])(?=.*\d)[A-Z][A-Za-z\d]{3,}$"

    if re.match(role_username, user.username) is not None:
        if re.match(role_password, user.password) is not None:
            try:
                postData = create_user(user)
                if postData:
                    return success_post_data(1, "Register Success")

                return post_data_fail("Create Accunt Gagal")
            except:
                post_data_fail("Create Account Gagal")
        else:
            return post_data_fail(
                "Password harus mengandung kombinasi angka dan huruf, harus diawali huruf besar, memiliki lebih dari 3 karakter")
    else:
        return post_data_fail(
            "username harus mengandung 2 angka, memiliki lebih dari 6 karakter dan kurang dari 15 karakter")


@auth.post("/login/")
async def login_user(log: Login):
    data = login(log)
    if data["message"]:
        return get_data_null(data["message"])
    userInfo = {
        "username": data["username"],
        "id_user": data["id_user"],
        "nama_lengkap": data["nama_lengkap"]
    }
    return success_get_data(userInfo)
