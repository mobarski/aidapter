# REF: https://platform.openai.com/docs/api-reference/completions

from . import base
import openai
import sys
import os

def use_key(key):
	openai.api_key = key
if not openai.api_key:
	use_key(os.getenv('OPENAI_API_KEY',''))


class ChatModel(base.BaseModel):
    RENAME_KWARGS = {'limit':'max_tokens'}


    def complete_one(self, prompt, **kw) -> dict:
        kwargs = self.get_api_kwargs(kw)
        kwargs['stop'] = kwargs.get('stop') or None # FIX empty value
        kwargs['model'] = self.name
        #
        system = kw.get('system','')
        messages = []
        if system:
              messages += [{'role':'system', 'content':system}]
        messages += [{'role':'user', 'content':prompt}]
        kwargs['messages'] = messages
        #kwargs['max_tokens'] = limit # TODO
        #
        kwargs = self.rename_kwargs(kwargs)
        resp = openai.ChatCompletion.create(**kwargs)
        #
        out = {}
        out['text'] = resp['choices'][0]['message']['content']
        out['usage'] = resp['usage']
        out['kwargs'] = kwargs
        out['resp'] = resp
        return out


class TextModel(base.BaseModel):
     RENAME_KWARGS = {'limit':'max_tokens'}

     def complete_one(self, prompt, **kw) -> dict:
        kwargs = self.get_api_kwargs(kw)
        kwargs['stop'] = kwargs.get('stop') or None # FIX empty value
        kwargs['model'] = self.name
        #
        system = kw.get('system','')
        full_prompt = prompt if not system else f'{system.rstrip()}\n\n{prompt}'
        kwargs['prompt'] = full_prompt
        #
        kwargs = self.rename_kwargs(kwargs)
        resp = openai.Completion.create(**kwargs)
        #
        out = {}
        out['text'] = resp['choices'][0]['text']
        out['usage'] = resp['usage']
        out['kwargs'] = kwargs
        out['resp'] = resp
        return out
