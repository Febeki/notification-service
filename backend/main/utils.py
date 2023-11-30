import datetime as dt
from typing import Optional

import pytz
from django.utils import timezone


def _is_valid_timezone(timezone_name: str) -> bool:
    """validation timezone
    Example: timezone_name = 'Europe/Moscow'
    Return True
    Example 2: timezone_name = 'Check/12345'
    Return False
    """
    try:
        pytz.timezone(timezone_name)
        return True
    except pytz.UnknownTimeZoneError:
        return False


def time_to_send_message(client_timezone: str, start_time: dt.datetime, end_time: dt.datetime) -> Optional[dt.datetime]:
    """calculate the time of sending a message
    return datetime object or None"""
    if _is_valid_timezone(client_timezone) and start_time < end_time:
        server_tz = timezone.get_current_timezone()
        client_tz = pytz.timezone(client_timezone)
        client_time = dt.datetime.now(client_tz)
        client_time_without_timezone = client_time.replace(tzinfo=server_tz)

        if client_time_without_timezone < start_time:
            time_difference = client_time_without_timezone - timezone.now()
            start_task_at = start_time - time_difference
            return start_task_at
        if start_time <= client_time_without_timezone <= end_time:
            start_task_at = client_time.astimezone(server_tz)
            return start_task_at
    return None
