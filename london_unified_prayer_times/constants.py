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
    ISLAMIC_MONTHS = 'islamic_months'


class ConfigKeys(Enum):
    TIMES = 'times'
    PM_TIMES = 'pm_times'
    AMBIGIOUS_TIMES = 'ambigious_times'
    AMBIGIOUS_THRESHOLD = 'ambigious_threshold'
    TIMEZONE = 'timezone'
    DEFAULT_TIMES = 'default_times'
    JSON_DATA = 'json_data'
    JSON_GREGORIAN_DATE = 'json_gregorian_date'
    JSON_ISLAMIC_DAY = 'json_islamic_day'
    JSON_ISLAMIC_MONTH = 'json_islamic_month'
    JSON_ISLAMIC_YEAR = 'json_islamic_year'
    COLUMN_PADDING = 'column_padding'
    DIGIT_PADDING = 'digit_padding'


class ClickKeys(Enum):
    NAME = 'name'
    FORMAT_TIME = 'format_time'
    TIMEZONE = 'timezone'
    USE_TIMES = 'use_times'


DEFAULT_TIMETABLE = 'default'
