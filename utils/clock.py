import datetime
import time

import pytz
from crequest.middleware import CrequestMiddleware
from django.conf import settings
from django.utils import timezone

now = timezone.now()


class Clock:
    """
    System Clock utility class
    """

    def __init__(self):
        pass

    @staticmethod
    def now():
        # return datetime.datetime(2014, 12, 31)
        return timezone.now()

    @staticmethod
    def utcnow():
        # return datetime.datetime(2014, 12, 31)
        return datetime.datetime.utcnow()

    @staticmethod
    def timestamp(_format="ms"):
        if _format == "ms":
            return int(time.time() * 1000)
        return int(time.time())

    @staticmethod
    def localTzname():
        if time.daylight:
            offsetHour = time.altzone / 3600
        else:
            offsetHour = time.timezone / 3600
        return "Etc/GMT%+d" % offsetHour

    @staticmethod
    def get_utc_from_local_time(value=None):
        return datetime.datetime.utcfromtimestamp(value / 1000)

    @staticmethod
    def get_user_universal_time(value=None):
        request = CrequestMiddleware.get_request()
        user_tz_offset = request.c_tz_offset
        if value is None:
            return Clock.utcnow() - datetime.timedelta(minutes=int(user_tz_offset))
        else:
            time_value = datetime.datetime.utcfromtimestamp(value / 1000)
            return time_value - datetime.timedelta(minutes=int(user_tz_offset))

    @staticmethod
    def get_user_universal_timestamp(value=None, _format="ms"):
        user_universal_time = Clock.get_user_universal_time(value)
        timestamp = user_universal_time.timestamp()
        if _format == "ms":
            return int(timestamp * 1000)
        return int(timestamp)

    @staticmethod
    def get_timestamp_from_user_time(user_timestamp=None):
        request = CrequestMiddleware.get_request()
        user_tz_offset = request.c_tz_offset

        system_time = datetime.datetime.fromtimestamp(user_timestamp / 1000)
        tz = pytz.timezone(settings.TIME_ZONE)
        system_offset = tz.utcoffset(system_time)
        system_time += system_offset
        system_time += datetime.timedelta(minutes=int(user_tz_offset))
        return int(system_time.timestamp()) * 1000

    @staticmethod
    def human_readable_time(time):
        # takes hour as an integer format and returns human readable time for corresponding hour
        if time == 0:
            return "12:00AM"
        if time == 12:
            return "12:00PM"
        if time >= 12:
            return str(time - 12) + ":00PM"
        else:
            return str(time) + ":00AM"
