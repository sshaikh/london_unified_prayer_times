from enum import Enum


class TimetableKeys(Enum):
    DATES = 'dates'
    ISLAMIC_DATES = 'islamicdates'
    TODAY = 'today'
    TOMORROW = 'tomorrow'
    TIMES = 'times'
    SOURCE = 'source'
    NAME = 'name'
    SETUP = 'setup'
    CONFIG = 'config'
    SCHEMA = 'schema'
    NUMBER_OF_DATES = 'num_dates'
    STATS = 'stats'
    MIN_DATE = 'min_date'
    MAX_DATE = 'max_date'


class ConfigKeys(Enum):
    TIMES = 'times'
    PM_TIMES = 'pm_times'
    AMBIGIOUS_TIMES = 'ambigious_times'
    AMBIGIOUS_THRESHOLD = 'ambigious_threshold'
    TIMEZONE = 'timezone'


class ClickKeys(Enum):
    NAME = 'name'
    FORMAT_TIME = 'format_time'
    TIMEZONE = 'timezone'


JSON_DATA = 'data'
JSON_GREGORIAN_DATE = 'gregoriandate'
JSON_ISLAMIC_DAY = 'islamicday'
JSON_ISLAMIC_MONTH = 'islamicmonth'
JSON_ISLAMIC_YEAR = 'islamicyear'
DEFAULT_TIMETABLE = 'default'
