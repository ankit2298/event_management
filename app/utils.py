# app/utils.py
from pytz import timezone, utc
from config import Config
from datetime import datetime

def to_ist(dt):
    tz = timezone(Config.TIMEZONE)
    return dt.astimezone(tz)

def from_ist(dt_str):
    tz = timezone(Config.TIMEZONE)
    dt = datetime.fromisoformat(dt_str)
    return tz.localize(dt).astimezone(utc)
