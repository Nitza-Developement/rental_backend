from datetime import datetime

import pytz
from django.conf import settings


def get_datetime_str_form_in_proper_area(date_field: datetime) -> str:
    date_local = date_field.astimezone(pytz.timezone(settings.TIME_ZONE))
    date_str = date_local.strftime("%d-%m-%Y - %H:%M:%S")
    return date_str
