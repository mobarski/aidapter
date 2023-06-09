from . import base
import transformers
import torch
import sys
import os

def use_key(key):
	pass


class TextModel(base.CompletionModel):
    RENAME_KWARGS  = {'limit':'max_new_tokens'}

    def __init__(self, name, kwargs, options):
        super().__init__(name, kwargs)
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(name)
        # OPTIONS
        kw = {}
        if '16bit' in options:
            kw['torch_dtype'] = torch.float16
        elif 'bloat16' in options:
            kw['torch_dtype'] = torch.bfloat16
        elif '8bit' in options:
            kw['load_in_8bit'] = True
        elif '4bit' in options:
            kw['load_in_4bit'] = True
        else:
             kw['torch_dtype'] = 'auto'
        if 'trust' in options:
            kw['trust_remote_code'] = True
        self.model = transformers.AutoModelForCausalLM.from_pretrained(name, device_map="auto", **kw)

    def transform_one(self, prompt, **kw) -> dict:
        kwargs = self.get_api_kwargs(kw)
        kwargs['stop'] = kwargs.get('stop') or [] # FIX empty value
        kwargs['model'] = self.name
        # full_prompt
        system = kw.get('system','')
        start = kw.get('start','')
        full_prompt = prompt if not system else f'{system.rstrip()}\n\n{prompt}'
        full_prompt += start
        kwargs['prompt'] = full_prompt
        #
        #kwargs = self.rename_kwargs(kwargs) # NOT USED - direct mapping below
        final_kwargs = dict(
            max_new_tokens = kwargs['limit'],
            temperature = kwargs['temperature'],
            pad_token_id = self.tokenizer.eos_token_id,
        )
        # stop early if stop criteria is met
        if kwargs['stop']:
            def stop_fun(ids, scores, **_):
                output_text = self.tokenizer.decode(ids[0])[len(full_prompt):]
                for s in kwargs['stop']:
                    if s in output_text:
                        return True
            final_kwargs['stopping_criteria'] = [stop_fun]
        #
        prompt_tokens = self.tokenizer.encode(full_prompt, return_tensors='pt')
        resp = self.model.generate(
                prompt_tokens.to("cuda"),
                **final_kwargs
            )
        resp_text = self.tokenizer.decode(resp[0], skip_special_tokens=True)
        output_text = resp_text[len(full_prompt):]
        # remove stop criteria from output
        if kwargs['stop']:
            for s in sorted(kwargs['stop'], key=lambda x: len(x), reverse=True):
                if s in output_text:
                    output_text = output_text.split(s)[0]
        #
        out = {}
        out['output'] = start + output_text
        out['usage'] = {
            'prompt_tokens': prompt_tokens.shape[1],
            'resp_tokens': resp.shape[1],
            'total_tokens': prompt_tokens.shape[1] + resp.shape[1],
            'prompt_chars': len(full_prompt),
            'resp_chars': len(out['output']),
            'total_chars': len(full_prompt) + len(out['output']),
        }
        out['kwargs'] = final_kwargs
        out['resp'] = {'resp':resp, 'prompt_tokens':prompt_tokens}
        # TODO usage
        # TODO error
        return out

    def raw_embed_one(self, text, **kw):
        input = self.tokenizer.encode(text, return_tensors='pt')
        outputs = self.model(input, output_hidden_states=True)
        last_hidden_state = outputs.hidden_states[-1][0]
        fun = lambda x: x[0].tolist()
        return fun(last_hidden_state)
