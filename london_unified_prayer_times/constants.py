from enum import Enum


class TimetableKeys(Enum):
    DATES = 'dates'
    ISLAMIC_DATES = 'islamicdates'
    TODAY = 'today'
    TOMORROW = 'tomorrow'
    TIMES = 'times'
    SOURCE = 'source'


class ConfigKeys(Enum):
    PRAYERS = 'prayers'
    PM_PRAYERS = 'pm_prayers'
    AMBIGIOUS_PRAYERS = 'ambigious_prayers'
    AMBIGIOUS_THRESHOLD = 'ambigious_threshold'
    TIMEZONE = 'timezone'


JSON_DATA = 'data'
JSON_GREGORIAN_DATE = 'gregoriandate'
JSON_ISLAMIC_DAY = 'islamicday'
JSON_ISLAMIC_MONTH = 'islamicmonth'
JSON_ISLAMIC_YEAR = 'islamicyear'
PICKLE_FILENAME = 'timetable.pickle'
