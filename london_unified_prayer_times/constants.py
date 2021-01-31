from enum import Enum


class TimetableKeys(Enum):
    DATES = 'dates'
    ISLAMIC_DATES = 'islamicdates'
    TODAY = 'today'
    TOMORROW = 'tomorrow'
    TIMES = 'times'
    SOURCE = 'source'
    NAME = 'name'
    CONFIG = 'config'
    SCHEMA = 'schema'
    NUMBER_OF_DATES = 'num_dates'


class ConfigKeys(Enum):
    TIMES = 'times'
    PM_TIMES = 'pm_times'
    AMBIGIOUS_TIMES = 'ambigious_times'
    AMBIGIOUS_THRESHOLD = 'ambigious_threshold'
    TIMEZONE = 'timezone'


JSON_DATA = 'data'
JSON_GREGORIAN_DATE = 'gregoriandate'
JSON_ISLAMIC_DAY = 'islamicday'
JSON_ISLAMIC_MONTH = 'islamicmonth'
JSON_ISLAMIC_YEAR = 'islamicyear'
PICKLE_FILENAME = 'timetable'
