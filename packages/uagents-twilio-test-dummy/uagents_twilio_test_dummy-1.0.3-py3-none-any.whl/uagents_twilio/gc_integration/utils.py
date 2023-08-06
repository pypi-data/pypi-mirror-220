from datetime import date, datetime, time
from typing import Union

from dateutil.parser import parse
from pytz import timezone as get_timezone
from tzlocal import get_localzone_name


def ensure_localisation(
    dt: Union[date, datetime], timezone: str = get_localzone_name()
) -> Union[date, datetime]:
    """Ensure localisation with provided timezone on "datetime" object.

    Does nothing to object of type "date"."""

    if isinstance(dt, datetime):
        tz = get_timezone(timezone)
        if dt.tzinfo is None:
            dt = tz.localize(dt)
        return dt
    elif isinstance(dt, date):
        return dt
    else:
        raise TypeError(
            '"date" or "datetime" object expected, not {!r}.'.format(
                dt.__class__.__name__
            )
        )


def to_localized_iso(
    dt: Union[date, datetime], timezone: str = get_localzone_name()
) -> str:
    """Return localised datetime object as iso formatted string"""
    if not isinstance(dt, datetime):
        dt = datetime.combine(dt, time())
    return ensure_localisation(dt, timezone).isoformat()


def get_datetime_from_string(date_str: str) -> datetime:
    """Convert datetime string to datetime"""
    return parse(date_str)
