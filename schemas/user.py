from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Register(BaseModel):
    nama_lengkap: str
    username: str
    password: str
