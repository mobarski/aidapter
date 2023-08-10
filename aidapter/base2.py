from multiprocessing.dummy import Pool
from retry import retry

# TODO: keys ???
# TODO: kwargs vs options ???
# DONE: iter vs list vs single
# DONE: as_iter
# DONE: kwargs
# DONE: usage
# DONE: retry
# DONE: cache
# DONE: progress
# DONE: batch
# DONE: workers

class BaseModelV2:

    def __init__(self, name, kwargs, options):
        "Initialize a model."
        self.name = name
        self.brand = 'base-v2'
        self.usage = {}
        self.cache = {}
        self.workers = 2
        self.batch = 4
        self.options = options
        self.model_kwargs = kwargs
        self.retry_kwargs = None
        self.memoize_kwargs = {'name':f'{name}:default'}


    def transform(self, inputs:str|list[str], as_iter=False, **kwargs):
        "Transform a single input or a list of inputs."
        if isinstance(inputs, str):
            return list(self.transform_many([inputs], **kwargs))[0]
        elif as_iter:
            return self.transform_many(inputs, **kwargs) # returns generator
        else:
            return list(self.transform_many(inputs, **kwargs))


    def transform_many(self, inputs: list[str], **kwargs):
        "Transform a list of inputs in batches / parallel workers."
        data = inputs if self.batch == 1 else batched(inputs, self.batch)
        
        # build worker
        def worker(_inputs):
            return self.transform_batch(_inputs, **kwargs)
        if self.retry_kwargs:
            worker = retry(**self.retry_kwargs)(worker)
        if kwargs.get('cache',True):
            worker = self.get_memoize()(worker)
        
        # run workers
        with Pool(self.workers) as pool:
            for resp in pool.imap(worker, data):
                yield from resp
    

    def transform_batch(self, inputs, **kwargs):
        "Transform a batch of inputs (MOCK implementation)"
        from time import sleep
        sleep(0.5)
        resp = inputs
        self.register_usage({'api-calls':1})
        return resp
    
    # # #

    def register_usage(self, kv: dict):
        "Register usage metrics."
        for k,v in kv.items():
            key = self.get_usage_key(k)
            incr(self.usage, key, v)

    # # #

    def get_memoize(self):
        "Get a memoization function."
        try:
            return self.cache.memoize(**self.memoize_kwargs)
        except:
            return lambda x:x

    def get_usage_key(self, k):
        "Get a key for a given metric that will be tracked in the usage key-value store."
        return f'{k}:{self.brand}:{self.name}'

# HELPERS

from itertools import islice

def batched(data, n, as_type=list):
    "Batch an iterable into fixed-length chunks."
    it = iter(data)
    while batch := as_type(islice(it, n)):
        yield batch

def incr(obj, key, val):
    "Increment a value in a dict or diskcache (for tracking usage)"
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
    m.batch = 2
    m.workers = 1
    print(m.transform('XXX'))
    print(m.transform(['YYY']))
    print(m.transform(['AAA','BBB']))
    for data in ["11 22 33 44 55 66 77 88 99".split(' '), ['XX'], 'YY']:
        pg = tqdm(total=len(data))
        out = m.transform(data, as_iter=True)
        for x in out:
            pg.update(1)
            print(x)
    print(m.usage)
