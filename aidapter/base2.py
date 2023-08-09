from multiprocessing.dummy import Pool
from retry import retry

# TODO: keys
# TODO: kwargs vs options
# DONE: kwargs
# DONE: usage
# DONE: retry
# DONE: cache
# DONE: progress
# DONE: batch
# DONE: workers

class BaseModelV2:

    def __init__(self, name, kwargs, options):
        self.name = name
        self.usage = {}
        self.cache = {}
        self.workers = 2
        self.batch = 4
        self.options = options
        self.model_kwargs = kwargs
        self.retry_kwargs = None
        self.memoize_kwargs = {'name':f'{name}:default'}

    def transform_many(self, inputs, **kwargs):
        if just_one := isinstance(inputs, str):
            inputs = [inputs]
        data = inputs if self.batch == 1 else batched(inputs, self.batch)

        # build worker
        def worker(_inputs):
            return self.transform_batch(_inputs, **kwargs)
        if self.retry_kwargs:
            worker = retry(**self.retry_kwargs)(worker)
        if kwargs.get('cache',True):
            worker = self.get_memoize()(worker)

        out = []
        with Pool(self.workers) as pool:
            for resp in pool.imap(worker, data):
                out.extend(resp)
                self.register_progress(len(out))
        
        return out[0] if just_one else out
    

    def transform_batch(self, inputs, **kwargs):
        # MOCK implementation
        resp = inputs
        self.register_usage({'api-calls':1})
        return resp
    
    # # #

    def register_usage(self, kv: dict):
        for k,v in kv.items():
            key = self.get_usage_key(k)
            incr(self.usage, key, v)

    def register_progress(self, done):
        pass # MOCK implementation

    # # #

    def get_memoize(self):
        try:
            return self.cache.memoize(**self.memoize_kwargs)
        except:
            return lambda x:x

    def get_usage_key(self, k):
        return f'{k}:{self.name}'

# HELPERS

from itertools import islice

def batched(data, n, as_type=list):
    "Batch an iterable into fixed-length chunks."
    it = iter(data)
    while batch := as_type(islice(it, n)):
        yield batch

def incr(obj, key, val):
    "Increment a value in a dict or diskcache."
    if hasattr(obj, 'incr'):
        obj.incr(key, val)
    else:
        obj[key] = obj.get(key,0) + val

# === SANDBOX =====================================================================================

if __name__=='__main__':
    import diskcache as dc
    from functools import partial
    from tqdm import tqdm

    m = BaseModelV2('test',{},{})
    pg = tqdm(total=100)
    m.register_progress = pg.update
    out = m.transform_many("11 22 33 44 55 66 77 88 99".split(' '))
    print(out)
    print(m.usage)
