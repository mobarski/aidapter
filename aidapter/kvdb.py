import os
import shelve


class DummyKV(dict):
    "in-memory key-value store"

    def sync(self):
        pass

    def close(self):
        self.sync()


# TODO: remove
class PKV:
    "persistent prefix-key-value store (based on the shelve module)"
    separator = '/'

    def __init__(self, path, prefix=''):
        self.prefix = prefix
        root = os.path.dirname(path)
        try:
            os.makedirs(root)
        except:
            pass
        self.db = shelve.open(path, flag='c')

    def __getitem__(self, key):
        return self.db[self._key(key)]

    def __setitem__(self, key, value):
        self.db[self._key(key)] = value

    def __delitem__(self, key):
        del self.db[self._key(key)]
    
    def __contains__(self, key):
        return self._key(key) in self.db

    def __repr__(self):
        return dict(self.items()).__repr__()

    def get(self, key, default=None):
        return self.db.get(self._key(key), default)

    def keys(self):
        return (k[len(self.prefix+self.separator):] for k in self.db.keys() if k.startswith(self.prefix+self.separator))

    def values(self):
        return (v for k,v in self.db.items() if k.startswith(self.prefix+self.separator))

    def items(self):
        return ((k[len(self.prefix+self.separator):],v) for k,v in self.db.items() if k.startswith(self.prefix+self.separator))

    #

    def sync(self):
        self.db.sync()
    
    def close(self):
        self.db.close()

    def _key(self, key):
        return f'{self.prefix}{self.separator}{key}'


# TODO: remove
class KV(PKV):
    "persistent key-value store (based on the pickle module)"
    separator = ''
    def __init__(self, path):
        super().__init__(path, prefix='')



if __name__=="__main__":
    #db['a'] = 1
    #db['b'] = 2
    #db.sync()
    db = KV('usunmnie/kv.text')
    #db = PKV('usunmnie/db3.shelve', 'xxx')
    db['x'] = 42
    db['y'] = 123
    print(db['x'])
    print(db['y'])
    #del db['x']
    print(list(db.keys()))
    print(list(db.values()))
    print(list(db.items()))
    print(list(db.db.items()))
    print(db.get('z',777))
    print(db)
