# REF: https://console.anthropic.com/docs/api/reference

from . import base
import anthropic
import sys
import os

def use_key(key):
	anthropic.api_key = key
if not getattr(anthropic, 'api_key', None):
	use_key(os.getenv('ANTHROPIC_API_KEY',''))

class ChatModel(base.BaseModel):
    RENAME_KWARGS  = {'stop':'stop_sequences', 'limit':'max_tokens_to_sample'}

    def __init__(self, name, kwargs):
        super().__init__(name, kwargs)
        self.client = anthropic.Client(anthropic.api_key)

    def complete_one(self, prompt, **kw) -> dict:
        kwargs = self.get_api_kwargs(kw)
        kwargs['stop'] = kwargs.get('stop') or [] # FIX empty value
        kwargs['model'] = self.name
        #
        system = kw.get('system','')
        full_prompt = prompt if not system else f'{system.rstrip()}\n\n{prompt}'
        kwargs['prompt'] = f"{anthropic.HUMAN_PROMPT} {full_prompt}{anthropic.AI_PROMPT}"
        #
        kwargs = self.rename_kwargs(kwargs)
        resp = self.client.completion(**kwargs)
        #
        out = {}
        out['text'] = resp.get('completion','')
        out['usage'] = {
            'prompt_tokens': anthropic.count_tokens(kwargs['prompt']),
            'resp_tokens': anthropic.count_tokens(out['text']),
            'total_tokens': anthropic.count_tokens(kwargs['prompt']) + anthropic.count_tokens(out['text']),
            'prompt_chars': len(kwargs['prompt']),
            'resp_chars': len(out['text']),
            'total_chars': len(kwargs['prompt']) + len(out['text']),
        }
        out['kwargs'] = kwargs
        out['resp'] = resp
        # TODO usage
        # TODO resp['error']
        return out
