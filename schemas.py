# schemas.py
from pydantic import BaseModel

class PurchaseRequest(BaseModel):
    product_code: str
    quantity: int