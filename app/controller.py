from typing import Any, Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, literal

from . import models, types

GROUP_BY_FN = {
    "1hour": ["%H", 3600],
    "1minute": ["%M", 60]
}

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

    query = db\
        .query(models.Fill)\
        .filter(*filters)\

    return query.all()

def get_fills_in_range_group(db: Session, start_timestamp: str, end_timestamp: str, symbol: Optional[str], exchange: Optional[str], group_by: Optional[str]) -> List[Tuple[float, Any]]:
    filters = [
        models.Fill.timestamp > start_timestamp,
        models.Fill.timestamp <= end_timestamp
    ]

    if symbol:
        filters.append(models.Fill.symbol == symbol)

    if exchange:
        filters.append(models.Fill.exchange == exchange)

    group_by_operator, epoch_scale = GROUP_BY_FN.get(group_by, ["%H", 3600])
    timestamp = func.datetime(((models.Fill.timestamp / 1000000) / epoch_scale ) * epoch_scale, 'unixepoch')
    
    query = db\
        .query(
            func.sum(models.Fill.fill_price),
            func.sum(models.Fill.fees),
            timestamp
        )\
        .filter(*filters)\
        .group_by(func.strftime(group_by_operator, timestamp))

    return query.all()