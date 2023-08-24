from pydantic import BaseModel


class Pos(BaseModel):
    id_inv: str
    total_qty: int
