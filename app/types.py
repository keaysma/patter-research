from typing import List
from pydantic import BaseModel
from datetime import datetime

class Fill(BaseModel):
    order_id: int
    fill_price: float
    fill_quantity: float
    side: str 
    exchange: str
    symbol: str
    fees: float
    timestamp: datetime

    class Config:
        orm_mode = True

class FillList(BaseModel):
    fills: List[Fill]
    count: int