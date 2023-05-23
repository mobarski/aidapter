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

    def __init__(self, name, kwargs):
        self.name = name
        self.cache = DummyKV()
        self.usage = DummyKV()
        self.kwargs = kwargs
        self.retry_tries = 5
        self.retry_delay = 0.1
        self.retry_backoff = 3

    def complete(self, prompt, **kw):
        if type(prompt)==str:
            resp = self.complete_one_cached(prompt, **kw)
            out = resp['text']
        else:
            resp = self.complete_many(prompt, **kw)
            out = [x['text'] for x in resp]
        self.usage.sync() # TODO: only if changed
        self.cache.sync() # TODO: only if changed
        return out

    # MOCK / TO OVERRIDE

    def complete_one(self, prompt, system='', limit=100, stop=None, temperature=0.0) -> dict:
        # mock
        full_prompt = f'{system}\n\n{prompt}' if system else prompt
        #
        resp = {}
        from time import sleep
        sleep(1)
        resp['text'] = f'{full_prompt} DUMMY RESPONSE'
        resp['usage'] = {'dummy_tokens': 3}
        return resp

    # INTERNAL

    def complete_one_retry(self, prompt, system='', limit=100, stop=None, temperature=0.0) -> dict:
        return retry_call(
            self.complete_one,
            fargs=[prompt],
            fkwargs={'system':system, 'limit':limit, 'stop':stop, 'temperature':temperature},
            tries=self.retry_tries,
            delay=self.retry_delay,
            backoff=self.retry_backoff,
        )

    def complete_one_cached(self, prompt, system='', limit=100, stop=None, temperature=0.0, register=True) -> dict:
        if temperature!=0.0:
            resp = self.complete_one_retry(prompt, system=system, limit=limit, stop=stop, temperature=temperature)
            resp['usage'] = resp.get('usage', {})
            resp['usage']['cache_skip'] = 1
        else:
            cache_key = md5(f'{prompt}/{system}/{limit}/{stop}')
            if cache_key in self.cache:
                resp = self.cache[cache_key]
                resp['usage'] = {f'cached_{k}':v for k,v in resp.get('usage',{}).items() if 'cache' not in k}
                resp['usage']['cache_hit'] = 1
            else:
                resp = self.complete_one_retry(prompt, system=system, limit=limit, stop=stop, temperature=temperature)
                resp['usage'] = resp.get('usage', {})
                resp['usage']['cache_miss'] = 1
                self.cache[cache_key] = resp
        if register:
            self.register_usage(resp['usage'])
        return resp

    def complete_many(self, prompts, system='', limit=100, stop=None, temperature=0.0, workers=4, verbose=False) -> list[dict]:
        def worker(prompt):
            return self.complete_one_cached(prompt, system=system, limit=limit, stop=stop, temperature=temperature, register=False)
        with Pool(workers) as pool:
            out = []
            with tqdm(total=len(prompts), disable=not verbose) as pbar:
                for x in pool.imap(worker, prompts):
                    out.append(x)
                    self.register_usage(x.get('usage',{}))
                    pbar.update()
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
    m = BaseModel()
    print(m.complete(range(13), verbose=True))
    print('-'*80)
    print(m.complete(range(13), verbose=True))
    print('-'*80)
    print(m.complete(range(6), verbose=True, temperature=1.0))
    print('-'*80)
    print(m.cache)
    print('-'*80)
    print(m.usage)
