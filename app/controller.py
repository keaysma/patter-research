from typing import Any, Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, literal

from . import models, types

GROUP_BY_FN = {
    "1hour": ["%H", 3600],
    "1minute": ["%M", 60]
}

def get_fill(db: Session, timestamp: str) -> Optional[models.Fill]:
    """
    Gets one row from the fills table by primary key (timestamp)

    Args:
        db: Database Session
        timestamp: The primary key to query for

    Returns:
        An order fill or None, depending on the query result
    """
    return db.query(models.Fill).filter(models.Fill.timestamp == timestamp).one_or_none()

def get_fills_in_range(db: Session, start_timestamp: str, end_timestamp: str, symbol: Optional[str], exchange: Optional[str]) -> List[models.Fill]:
    """
    Gets a list of fills within a date and time range,
    handles filtering on symbol and exchange.

    Filters are optional

    Args:
        db: Database Session
        start_timestamp: Minimum timestamp/start of range, exclusive
        end_timestamp: Maximum timestamp/end of range, inclusive
        symbol: The symbol to filter on
        exchange: The exchange to filter on

    Returns:
        A list of order fills
    """
    
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
    """
    (WIP/NOT READY)
    Gets a list of fills within a date and time range,
    handles filtering on symbol and exchange.
    This function also accepts a group by key to group fill results

    Filters are optional

    Group by will sum fill prices, but doesn't account for side, hence, why this isn't ready

    Args:
        db: Database Session
        start_timestamp: Minimum timestamp/start of range, exclusive
        end_timestamp: Maximum timestamp/end of range, inclusive
        symbol: The symbol to filter on
        exchange: The exchange to filter on
        group_by: The granularity of the grouping (see GROUP_BY_FN)

    Returns:
        A list tuples, each tuple containing fill price, fees, and a timestamp
    """
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