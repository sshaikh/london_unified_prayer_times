import appdirs
import os
import pickle
from . import remote_data
from . import timetable


def get_cache_fileinfo(pickle_filename):
    cache_dir = appdirs.user_cache_dir(__package__)
    cache_file = cache_dir + '/' + pickle_filename + '.pickle'
    return cache_dir, cache_file


def cache_timetable(timetable, pickle_filename):
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


def refresh_timetable(url, schema, config, pickle_filename):
    json = remote_data.get_json_data(url, schema)
    built_timetable = timetable.build_timetable(url, json, config)
    cache_timetable(built_timetable, pickle_filename)
    return built_timetable
