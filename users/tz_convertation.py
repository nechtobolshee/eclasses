import pytz
from .middlewares import get_current_timezone


def convert_datetime_to_user_timezone(date_time):
    """
    Convert date to current user timezone.
    """
    print(date_time)
    current_timezone = get_current_timezone()
    local = pytz.timezone(current_timezone)
    date_time = date_time.astimezone(local)
    print(date_time)
    return date_time


def convert_datetime_to_utc_timezone(date_time):
    """
    Convert date to utc timezone.
    """
    user_tz = pytz.timezone(get_current_timezone())
    localized_time = user_tz.localize(date_time.replace(tzinfo=None))
    localized_time = localized_time.astimezone(pytz.utc)
    return localized_time
