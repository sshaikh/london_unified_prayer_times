import appdirs
import os
import pickle
import datetime
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
    try:
        os.remove(cache_file)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

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
    cutoff = datetime.datetime.utcnow() - delta

    if last_updated < cutoff:
        tt = refresh_timetable(tt)

    return tt


def init_timetable(name, source, config, schema):
    json = remote_data.get_json_data(source, schema)
    built_timetable = timetable.build_timetable(name, source,
                                                config, schema,
                                                json)
    cache_timetable(built_timetable)
    return built_timetable


def refresh_timetable(timetable):
    setup = timetable[tk.SETUP]
    url = setup[tk.SOURCE]
    schema = setup[tk.SCHEMA]
    config = setup[tk.CONFIG]
    name = timetable[tk.NAME]
    try:
        return init_timetable(name, url, config, schema)
    except Exception:
        return load_cached_timetable(name)


def refresh_timetable_by_name(name):
    timetable = load_cached_timetable(name)
    return refresh_timetable(timetable)
