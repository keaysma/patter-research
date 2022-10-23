from typing import Optional, List
from sqlalchemy.orm import Session

from . import models, types


def get_fill(db: Session, timestamp: str) -> Optional[models.Fill]:
    return db.query(models.Fill).filter(models.Fill.timestamp == timestamp).one_or_none()

def get_fills_in_range(db: Session, start_timestamp: str, end_timestamp: str, symbol: Optional[str], exchange: Optional[str]) -> List[models.Fill]:
    filters = [
        models.Fill.timestamp > start_timestamp,
        models.Fill.timestamp <= end_timestamp
    ]

    if symbol:
        filters.append(models.Fill.symbol == symbol)

    if exchange:
        filters.append(models.Fill.exchange == exchange)
    
    return db\
        .query(models.Fill)\
        .filter(*filters)\
        .all()