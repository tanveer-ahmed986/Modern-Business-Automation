"""Business-local time helpers.

MBAS stores all timestamps as naive UTC (datetime.utcnow()). The business
runs in the server's local timezone (offline, single-site installs), so
"today" and report date ranges must be computed over the LOCAL calendar day
and then converted to UTC bounds for querying.

Previously "today" was computed as date.today() combined with naive
midnight — local dates compared against UTC timestamps — which shifted
every day boundary by the UTC offset (e.g. sales before 05:00 PKT counted
toward the previous day).
"""

from datetime import date, datetime, time, timedelta
from typing import Optional, Tuple


def _local_tzinfo():
    """The server's local timezone (the business timezone for local installs)."""
    return datetime.now().astimezone().tzinfo


def utc_now() -> datetime:
    """Naive UTC now — matches the storage convention used across models."""
    return datetime.utcnow()


def local_today() -> date:
    """Today's date in the business-local timezone."""
    return datetime.now(_local_tzinfo()).date()


def local_day_utc_bounds(day: Optional[date] = None) -> Tuple[datetime, datetime]:
    """Naive-UTC [start, end) bounds of a business-local calendar day.

    Defaults to the local today. The end bound is exclusive (start of the
    next local day) so queries use `>= start AND < end` without the
    microsecond-truncation pitfalls of datetime.max.
    """
    if day is None:
        day = local_today()
    tz = _local_tzinfo()
    start_local = datetime.combine(day, time.min, tzinfo=tz)
    end_local = start_local + timedelta(days=1)
    # Convert to naive UTC to match the storage convention
    start = datetime.utcfromtimestamp(start_local.timestamp())
    end = datetime.utcfromtimestamp(end_local.timestamp())
    return start, end


def local_range_utc_bounds(
    start_day: Optional[date], end_day: Optional[date], default_days: int = 30
) -> Tuple[datetime, datetime]:
    """Naive-UTC [start, end) bounds covering local days start_day..end_day
    inclusive. Missing end defaults to local today; missing start defaults to
    `default_days` days before the end day."""
    if end_day is None:
        end_day = local_today()
    if start_day is None:
        start_day = end_day - timedelta(days=default_days)
    start, _ = local_day_utc_bounds(start_day)
    _, end = local_day_utc_bounds(end_day)
    return start, end


def local_date_key(dt_utc: Optional[datetime] = None) -> str:
    """YYYYMMDD key of the business-local day for a naive-UTC timestamp
    (defaults to now). Used for invoice numbering so invoices roll over at
    local midnight, not UTC midnight."""
    if dt_utc is None:
        return local_today().strftime("%Y%m%d")
    local_dt = dt_utc.replace(tzinfo=None)
    # naive UTC -> aware UTC -> local
    from datetime import timezone as _tz

    aware = local_dt.replace(tzinfo=_tz.utc).astimezone(_local_tzinfo())
    return aware.strftime("%Y%m%d")
