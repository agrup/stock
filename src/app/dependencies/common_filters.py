from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional


@dataclass
class PaginationParams:
    """Dataclass to hold common pagination parameters."""
    skip: int
    limit: int


@dataclass
class CommonFilterParams:
    """Dataclass to hold common filter parameters."""
    skip: int
    limit: int
    start_date: Optional[date]
    end_date: Optional[date]


def get_pagination_params(skip: int = 0, limit: int = 100) -> PaginationParams:
    """A dependency to gather common pagination parameters."""
    return PaginationParams(skip=skip, limit=limit)

def get_common_filters(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> CommonFilterParams:
    """A dependency to gather common filter parameters from query strings."""
    if start_date is None and end_date is None:
        # Default to the last 30 days if no date range is provided
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
    return CommonFilterParams(skip=skip, limit=limit, start_date=start_date, end_date=end_date)