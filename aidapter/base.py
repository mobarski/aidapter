from tqdm import tqdm
from retry.api import retry_call

from multiprocessing.dummy import Pool
import hashlib

# TODO:
# [x] usage
# [x] cache (shelve protocol = dict + sync/close)
# [x] cache usage -> cache_hit+=1 cache_miss+=1 cache_skip+=1
# [x] retry
# [ ] callbacks: before / after, one vs many
# [ ] start


class BaseModel:
    RENAME_KWARGS = {}

    def __init__(self, name, api_kwargs):
        self.kwargs = {
            'temperature': 0.0,
            'limit': 100,
            'stop': [],
        }
        self.kwargs.update(api_kwargs)
        self.name = name
        self.cache = DummyKV()
        self.usage = DummyKV()
        self.retry_tries = 5
        self.retry_delay = 0.1
        self.retry_backoff = 3
        self.workers = 4
        self.show_progress = False

    def complete(self, prompt, debug=False, **kw):
        if type(prompt)==str:
            resp = self.complete_one_cached(prompt, **kw)
            out = resp['text']
        else:
            resp = self.complete_many(prompt, **kw)
            out = [x['text'] for x in resp]
        self.usage.sync() # TODO: only if changed
        self.cache.sync() # TODO: only if changed
        if debug:
            return resp
        else:
            return out

    # MOCK / TO OVERRIDE

    def complete_one(self, prompt, **kw) -> dict:
        "mock"
        kwargs = self.get_api_kwargs(kw, ['temperature','stop','limit'])
        # mock
        system = kw.get('system','')
        full_prompt = f'{system}\n\n{prompt}' if system else prompt
        #
        kwargs = self.rename_kwargs(kwargs)
        from time import sleep
        sleep(1)
        resp = {}
        #
        resp['text'] = f'{full_prompt} DUMMY RESPONSE'
        resp['usage'] = {'dummy_tokens': 3}
        resp['kwargs'] = kwargs
        return resp

    # INTERNAL

    def get_api_kwargs(self, kw, kw_names=[]):
        kwargs = self.kwargs.copy()
        for k in kw_names:
            if k in kw:
                kwargs[k] = kw[k]
        return kwargs
    
    def rename_kwargs(self, kwargs):
        return {self.RENAME_KWARGS.get(k,k):v for k,v in kwargs.items()}

    def complete_one_retry(self, prompt, **kw) -> dict:
        return retry_call(
            self.complete_one,
            fargs=[prompt],
            fkwargs=kw,
            tries=self.retry_tries,
            delay=self.retry_delay,
            backoff=self.retry_backoff,
        )

    def complete_one_cached(self, prompt, register=True, **kw) -> dict:
        kwargs = self.get_api_kwargs(kw)
        if kwargs.get('temperature',0) != 0:
            resp = self.complete_one_retry(prompt, **kw)
            resp['usage'] = resp.get('usage', {})
            resp['usage']['cache_skip'] = 1
        else:
            kwargs_str = str([(k,kwargs[k]) for k in sorted(kwargs)])
            cache_key = md5(f'{prompt}/{kwargs_str}')
            if cache_key in self.cache:
                resp = self.cache[cache_key]
                resp['usage'] = {f'cached_{k}':v for k,v in resp.get('usage',{}).items() if 'cache' not in k}
                resp['usage']['cache_hit'] = 1
            else:
                resp = self.complete_one_retry(prompt, **kw)
                resp['usage'] = resp.get('usage', {})
                resp['usage']['cache_miss'] = 1
                self.cache[cache_key] = resp
        if register:
            self.register_usage(resp['usage'])
        return resp

    def complete_many(self, prompts, **kw) -> list[dict]:
        def worker(prompt):
            return self.complete_one_cached(prompt, register=False, **kw)
        with Pool(self.workers) as pool:
            out = []
            with tqdm(total=len(prompts), disable=not self.show_progress) as progress:
                for x in pool.imap(worker, prompts):
                    out.append(x)
                    self.register_usage(x.get('usage',{}))
                    progress.update()
        return out

    def register_usage(self, usage):
        if usage:
            self.usage.agg(usage)

# HELPERS

def md5(text):
    return hashlib.md5(text.encode()).hexdigest()

class DummyKV(dict):
    def sync(self):
        pass

    def close(self):
        pass

    def agg(self, mapping):
        if not mapping: return
        for k,v in mapping.items():
            if k not in self:
                self[k] = v
            else:
                self[k] += v

# QUICK TEST 

if __name__=="__main__":
    m = BaseModel('base',{'x':123})
    print(m.complete('hello', stop=['aa','bb'], debug=True))
    print(m.complete(range(13), verbose=True))
    print('-'*80)
    print(m.complete(range(13), verbose=True))
    print('-'*80)
    print(m.complete(range(6), verbose=True, temperature=1.0))
    print('-'*80)
    print(m.cache)
    print('-'*80)
    print(m.usage)
