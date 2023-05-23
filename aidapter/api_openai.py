from . import base
import openai
import os

def use_key(key):
	openai.api_key = key
if not openai.api_key:
	use_key(os.getenv('OPENAI_API_KEY',''))

class ChatModel(base.BaseModel):

    def complete_one(self, prompt, **kw) -> dict:
        system = kw.get('system','')
        #
        kwargs = self.kwargs.copy()
        kwargs['model'] = self.name
        for k in ['temperature','stop']:
            if k in kw:
                kwargs[k] = kw[k]
        #
        messages = []
        if system:
              messages += [{'role':'system', 'content':system}]
        messages += [{'role':'user', 'content':prompt}]
        kwargs['messages'] = messages
        #kwargs['max_tokens'] = limit # TODO
        #
        resp = openai.ChatCompletion.create(**kwargs)
        #
        out = {}
        out['text'] = resp['choices'][0]['message']['content']
        out['usage'] = resp['usage']
        return out
