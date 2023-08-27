import os
# import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.bahan_mentah_route.bahan_route import bahan
from routes.bahan_mentah_route.ukuran_route import ukuran
from routes.pos_route.pos_route import pos
from routes.produksi_route.produksi_route import produksi
from routes.inventory_route.inv_route import inv
from helper.exception import ExceptionHandler

load_dotenv()

app = FastAPI(
    title="Backend For Inventory App - API"
)

ExceptionHandler(app=app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inv)
app.include_router(produksi)
app.include_router(pos)
app.include_router(bahan)
app.include_router(ukuran)
