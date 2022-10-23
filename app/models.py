from sqlalchemy import Column, Integer, Text, Float, DateTime, String

from .database import Base

class Fill(Base):
    __tablename__ = 'fills'

    order_id = Column(Integer, nullable=False)
    fill_price = Column(Float, nullable=False)
    fill_quantity = Column(Float, nullable=False)
    side = Column(Text, nullable=False) #TEXT CHECK (side IN ('BUY', 'SELL')) NOT NULL,
    exchange = Column(Text, nullable=False)
    symbol = Column(Text, nullable=False)
    fees = Column(Float, nullable=False)
    timestamp = Column(String, primary_key=True)