import appdirs
import os
import pickle
import datetime
from zoneinfo import ZoneInfo
from . import remote_data
from . import timetable
from . import constants


tk = constants.TimetableKeys
ck = constants.ConfigKeys


def get_cache_fileinfo(pickle_filename):
    cache_dir = appdirs.user_cache_dir(__package__)
    cache_file = cache_dir + '/' + pickle_filename + '.pickle'
    return cache_dir, cache_file


def cache_timetable(timetable):
    pickle_filename = timetable[tk.NAME]
    cache_dir, cache_file = get_cache_fileinfo(pickle_filename)

    os.makedirs(cache_dir, exist_ok=True)

    if os.path.exists(cache_file):
        os.remove(cache_file)

    with open(cache_file, 'wb') as outfile:
        pickle.dump(timetable, outfile)


def load_cached_timetable(pickle_filename):
    cache_dir, cache_file = get_cache_fileinfo(pickle_filename)

    with open(cache_file, 'rb') as cached_pickle:
        return pickle.load(cached_pickle)


def load_timetable(name, refresh_delta):
    tt = load_cached_timetable(name)

    delta = refresh_delta
    if not delta:
        delta = tt[tk.SETUP][tk.CONFIG][ck.CACHE_EXPIRY]

    last_updated = tt[tk.STATS][tk.LAST_UPDATED]
    cutoff = datetime.datetime.utcnow().replace(tzinfo=ZoneInfo("UTC")) - delta

    if last_updated < cutoff:
        tt = refresh_timetable(tt)

    return tt


def init_timetable(name, source, config):
    data = remote_data.get_html_data(source, config[ck.HTML_TABLE_CSS_CLASS])
    built_timetable = timetable.build_timetable(name, source,
                                                config, data)
    cache_timetable(built_timetable)
    return built_timetable


def refresh_timetable(timetable):
    setup = timetable[tk.SETUP]
    url = setup[tk.SOURCE]
    config = setup[tk.CONFIG]
    name = timetable[tk.NAME]
    try:
        return init_timetable(name, url, config)
    except Exception:
        return load_cached_timetable(name)


def refresh_timetable_by_name(name):
    timetable = load_cached_timetable(name)
    return refresh_timetable(timetable)
