import pytz
from datetime import datetime
from .middlewares import get_current_timezone


def convert_datetime_to_user_timezone(date_time):
    """
    Convert date to current user timezone.
    """
    current_timezone = get_current_timezone()
    local = pytz.timezone(current_timezone)
    date_time = date_time.astimezone(local)
    return date_time


def convert_datetime_to_utc_timezone(date_time):
    """
    Convert date to utc timezone.
    """
    user_tz = pytz.timezone(get_current_timezone())
    localized_time = user_tz.localize(date_time.replace(tzinfo=None))
    localized_time = localized_time.astimezone(pytz.utc)
    return localized_time


def convert_time_to_user_timezone(time):
    """
    Convert time to current user timezone.
    """
    datetime_value = datetime.combine(date=datetime.today(), time=time)
    current_timezone = get_current_timezone()
    local = pytz.timezone(current_timezone)
    user_time = datetime_value.astimezone(local).time()
    return user_time


def convert_time_to_utc_timezone(time):
    """
    Convert time to utc timezone.
    """
    datetime_value = datetime.combine(date=datetime.today(), time=time)
    user_tz = pytz.timezone(get_current_timezone())
    localized_time = user_tz.localize(datetime_value.replace(tzinfo=None))
    localized_time = localized_time.astimezone(pytz.utc).time()
    return localized_time
