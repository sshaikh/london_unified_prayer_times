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
    LAST_UPDATED = 'last_updated'


class ConfigKeys(Enum):
    TIMES = 'times'
    PM_TIMES = 'pm_times'
    AMBIGIOUS_TIMES = 'ambigious_times'
    AMBIGIOUS_THRESHOLD = 'ambigious_threshold'
    TIMEZONE = 'timezone'
    DEFAULT_TIMES = 'default_times'
    DEFAULT_REPLACE_STRINGS = 'default_replace_strings'
    JSON_DATA_PATH = 'json_data_path'
    JSON_GREGORIAN_DATE = 'json_gregorian_date'
    JSON_ISLAMIC_DAY = 'json_islamic_day'
    JSON_ISLAMIC_MONTH = 'json_islamic_month'
    JSON_ISLAMIC_YEAR = 'json_islamic_year'
    CACHE_EXPIRY = 'cache_expiry'


class ClickKeys(Enum):
    NAME = 'name'
    FORMAT_TIME = 'format_time'
    HOURS = 'hours'
    TIMEZONE = 'timezone'
    USE_TIMES = 'use_times'
    CACHE_EXPIRY = 'cache_expiry'
    REPLACE_STRINGS = 'replace_strings'


DEFAULT_TIMETABLE = 'default'
COLUMN_PADDING = 4
