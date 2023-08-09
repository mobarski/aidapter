from tqdm import tqdm
from retry.api import retry_call

from multiprocessing.dummy import Pool
from itertools import islice
from datetime import date
from time import time
import hashlib

# TODO: callbacks: before / after, one vs many

# COMPLETION

class BaseModel:
    RENAME_KWARGS = {}
    DEFAULT_KWARGS = {}

    def __init__(self, name, api_kwargs, options=''):
        self.kwargs = self.DEFAULT_KWARGS.copy()
        self.kwargs.update(api_kwargs)
        self.options = options
        self.name = name
        self.cache = DummyKV()
        self.usage = DummyKV()
        self.retry_tries = 5
        self.retry_delay = 0.1
        self.retry_backoff = 3
        self.workers = 4
        self.batch = 1
        self.show_progress = False
        self.id = '' # this will be set by the factory function

    # INTERNAL

    def get_api_kwargs(self, kw):
        kwargs = self.kwargs.copy()
        for k in self.DEFAULT_KWARGS:
            if k in kw:
                kwargs[k] = kw[k]
        return kwargs
    
    def rename_kwargs(self, kwargs):
        return {self.RENAME_KWARGS.get(k,k):v for k,v in kwargs.items()}

    def register_usage(self, usage):
        if usage:
            keys = self.get_usage_keys()
            for key in keys:
                data = self.usage.get(key, {})
                use_incr = hasattr(data, 'incr')
                for k,v in usage.items():
                    if use_incr:
                        data.incr(k, v)
                    else:
                        data[k] = data.get(k,0) + v
                self.usage[key] = data

    def get_usage_keys(self):
        day = str(date.today()) # iso format
        keys = [
            f'total:{self.name}',
            f'day:{day}:{self.name}',
        ]
        return keys

    # TRANSFORM

    def transform(self, input, debug=False, cache='use', **kw):
        if type(input)==str:
            resp = self.transform_one_cached(input, cache=cache, **kw)
            out = resp['output']
        else:
            resp = self.transform_many(input, cache=cache, **kw)
            out = [x['output'] for x in resp]
        self.usage.sync() # TODO: only if changed
        self.cache.sync() # TODO: only if changed
        if debug:
            return resp
        else:
            return out

    def transform_one_retry(self, input, **kw) -> dict:
        return retry_call(
            self.transform_one,
            fargs=[input],
            fkwargs=kw,
            tries=self.retry_tries,
            delay=self.retry_delay,
            backoff=self.retry_backoff,
        )

    def transform_many(self, inputs, cache='use', **kw) -> list[dict]:
        def worker(prompt):
            return self.transform_one_cached(prompt, cache=cache, register=False, **kw)
        data = inputs if self.batch==1 else batched(inputs, self.batch)
        # TODO batched
        with Pool(self.workers) as pool:
            out = []
            with tqdm(total=len(data), disable=not self.show_progress) as progress:
                for x in pool.imap(worker, data):
                    out.append(x)
                    self.register_usage(x.get('usage',{}))
                    progress.update()
        return out

    # TODO: cache=save
    # TODO: dont save cache if empty
    def transform_one_cached(self, input, cache='use', register=True, **kw) -> dict:
        t0 = time()
        kwargs = self.get_api_kwargs(kw)
        cache_key = self.get_cache_key(input, kwargs, kw)
        if self.skip_cache_condition(kwargs, kw, cache):
            resp = self.transform_one_retry(input, **kw)
            resp['usage'] = resp.get('usage', {})
            resp['usage']['cache_skip'] = 1
        else:
            if cache_key in self.cache:
                resp = self.cache[cache_key]
                resp['usage'] = {f'cached_{k}':v for k,v in resp.get('usage',{}).items() if 'cache' not in k}
                resp['usage']['cache_hit'] = 1
            else:
                resp = self.transform_one_retry(input, **kw)
                resp['usage'] = resp.get('usage', {})
                resp['usage']['cache_miss'] = 1
                self.cache[cache_key] = resp
        resp['usage']['time'] = time() - t0
        if register:
            self.register_usage(resp['usage'])
        return resp

    def skip_cache_condition(self, kwargs, kw, cache):
        return cache in ('skip','save')

    def get_cache_key(self, input, kwargs, kw):
        all_kwargs = kwargs.copy()
        all_kwargs.update(kw)
        kwargs_str = str([(k,all_kwargs[k]) for k in sorted(all_kwargs)])
        cache_key = self.name +':'+ md5(f'{input}:{kwargs_str}')
        return cache_key


class CompletionModel(BaseModel):
    DEFAULT_KWARGS = {'temperature':0, 'stop':[], 'limit':100}

    def complete(self, prompt, debug=False, cache='use', **kw):
        return self.transform(prompt, debug=debug, cache=cache, **kw)

    def skip_cache_condition(self, kwargs, kw, cache):
        return (kwargs.get('temperature',0)!=0 or cache=='skip') and cache!='force'

    # MOCK

    def transform_one(self, prompt, **kw) -> dict:
        "mock"
        kwargs = self.get_api_kwargs(kw)
        # mock
        system = kw.get('system','')
        full_prompt = f'{system}\n\n{prompt}' if system else prompt
        #
        kwargs = self.rename_kwargs(kwargs)
        from time import sleep
        sleep(1)
        resp = {}
        #
        resp['output'] = f'{full_prompt} DUMMY RESPONSE'
        resp['usage'] = {'dummy_tokens': 3}
        resp['kwargs'] = kwargs
        return resp

# EMBEDDING

class EmbeddingModel(BaseModel):

    def embed(self, text, debug=False, cache='use', **kw):
        return self.transform(text, debug=debug, cache=cache, **kw)

    # MOCK

    def transform_one(self, text, debug=False, cache='use', **kw):
        limit = kw.get('limit')
        return {
            'output': [1,2,3,4,5][:limit],
        }

# HELPERS

def md5(text):
    return hashlib.md5(text.encode()).hexdigest()

def batched(data, n, as_type=list):
    it = iter(data)
    while batch := as_type(islice(it, n)):
        yield batch

class DummyKV(dict):
    "in-memory key-value store with shelve-like interface"
    def sync(self):
        pass
    def close(self):
        pass
