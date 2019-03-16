import pickle
from functools import wraps
from logging import info, debug


class Cache:
    data = {}

    def __init__(self, observable, file_name='authCache.cache'):
        self.observable = observable
        self.file_name = file_name

    def save_to_file(self):
        with open(self.file_name, 'wb+') as f:
            s = pickle.dumps(self.data)
            f.seek(0)
            f.write(s)
            f.truncate()
            f.flush()
        debug('%s updates flushed to file' % (self.observable.__repr__()))

    def read_from_file(self):
        with open(self.file_name, 'rb') as f:
            self.data = pickle.load(f)
        debug('%s cache %d item loaded' % (self.observable.__repr__(), self.data.__len__()))

    @staticmethod
    def hash_key(*args, **kwargs):
        args_repr = list(map(lambda x: x.__dict__.__repr__(), args))
        kwargs_repr = list(str(x) for x in kwargs.values())
        return '_'.join(args_repr) + '-' + '_'.join(kwargs_repr)

    def update(self, hash_key, func_result=None):
        debug('Updating cached item result')
        self.observable.cache.data[hash_key] = result = func_result
        self.save_to_file()
        return result


def cached(func): # TODO: rewrite to get file-name in decorator args; one-module = one-cache-file
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func.cache.read_from_file()
        except:
            info('No cache file')
        try:
            value = func.cache.data[func.cache.hash_key(*args, **kwargs)]
            debug('Returning cached result %s' % value)
            return value
        except:
            debug('Record not found in cache')
            result = func.cache.update(func.cache.hash_key(*args, **kwargs), func(*args, **kwargs))
            return result

    func.cache = Cache(func, func.__name__+'.cache')
    wrapper.cache = func.cache
    return wrapper
