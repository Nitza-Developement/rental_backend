from datetime import datetime
from typing import Optional

import pytz
from django.conf import settings


def get_datetime_str_form_in_proper_area(date_field: datetime) -> Optional[str]:
    if date_field is None:
        return None
    date_local = date_field.astimezone(pytz.timezone(settings.TIME_ZONE))
    date_str = date_local.strftime("%d-%m-%Y - %H:%M:%S")
    return date_str
