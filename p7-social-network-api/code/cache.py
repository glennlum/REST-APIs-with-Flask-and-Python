'''
[POC] Stand-in for an in-memory data structure store (eg. Redis)
'''
feed_cache = {}  # key: string, value: list of dictionaries

'''
[POC] Stand-in for an in-memory data structure store (eg. Redis)
'''
related_cache = {}  # key: int, value: list of dictionaries


class CacheManager():

    '''
    Contains a set of helper methods for cache reads/writes
    '''

    @classmethod
    def save_to_cache(cls, cache, key, value):
        '''
        Saves a key-value pair to the cache
        '''
        if key not in cache:
            cache[key] = [value]
        else:
            cache[key].append(value)

    @classmethod
    def find_by_key(cls, cache, key):
        '''
        Returns data associated with the given key
        '''
        if key not in cache:
            return False
        return cache[key]

    @classmethod
    def contains_key(cls, cache, key):
        '''
        Checks if the cache contains the given key
        '''
        if key not in cache:
            return False
        return True
