# REF: https://cohere.ai/pricing
# REF: https://dashboard.cohere.ai/api-keys
# REF: https://docs.cohere.ai/reference/generate
# REF: https://docs.cohere.ai/reference/embed
# REF: https://docs.cohere.ai/reference/tokenize

from . import base
import cohere
import sys
import os

def use_key(key):
	cohere.api_key = key
if not getattr(cohere, 'api_key', None):
	use_key(os.getenv('CO_API_KEY',''))

class TextModel(base.BaseModel):
    RENAME_KWARGS  = {'stop':'stop_sequences', 'limit':'max_tokens'}

    def __init__(self, name, kwargs):
        super().__init__(name, kwargs)
        self.client = cohere.Client(cohere.api_key)

    def complete_one(self, prompt, **kw) -> dict:
        kwargs = self.get_api_kwargs(kw)
        kwargs['stop'] = kwargs.get('stop') or [] # FIX empty value
        kwargs['model'] = self.name
        #
        system = kw.get('system','')
        full_prompt = prompt if not system else f'{system.rstrip()}\n\n{prompt}'
        kwargs['prompt'] = full_prompt
        #
        kwargs = self.rename_kwargs(kwargs)
        resp = self.client.generate(**kwargs)
        #
        out = {}
        out['text'] = resp[0]
        out['usage'] = {} # TODO
        out['kwargs'] = kwargs
        out['resp'] = resp
        # TODO usage
        # TODO error
        return out
