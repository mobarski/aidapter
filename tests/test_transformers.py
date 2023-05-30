import sys; sys.path[0:0] = ['.','..']
#import os
#os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128' # PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128 

import aidapter

#model_id = 'openai:text-ada-001'

# model_id = 'transformers:roneneldan/TinyStories-33M'
# model_id = 'transformers:RWKV/rwkv-raven-1b5'
#model_id = 'transformers:tiiuae/falcon-rw-1b:trust'
# model_id = 'transformers:RWKV/rwkv-raven-3b'
# model_id = 'transformers:TheBloke/guanaco-7B-HF:4bit'
# model_id = 'transformers:project-baize/baize-v2-7b:4bit'
# model_id = 'transformers:tiiuae/falcon-7b:trust'
# model_id = 'transformers:ehartford/Wizard-Vicuna-13B-Uncensored:4bit'
# model_id = 'transformers:ehartford/WizardLM-30B-Uncensored:4bit'
# model_id = 'transformers:timdettmers/guanaco-33b-merged:4bit'

from pprint import pprint
print(f'=== {model_id} ===')
model = aidapter.model(model_id)
model.retry_tries = 1
#print(model.complete('there was a little girl who', debug=False))
#print()
math_prompts = ['2+2=','7*6=','3-7=','2^8=']
pprint(model.complete(math_prompts, debug=False, limit=5, stop=[]))
pprint(model.complete(math_prompts, debug=False, limit=5, stop=["\n","2"]))
print(model.id)

# NOPE:
# model_id = 'transformers:RWKV/rwkv-raven-14b:8bit' # NOPE
# model_id = 'transformers:RWKV/rwkv-raven-14b:4bit' # NOPE
# model_id = 'transformers:openaccess-ai-collective/mpt-7b-replit-update:4bit,trust' # NOPE
# model_id = 'transformers:tiiuae/falcon-40b:4bit,trust' # NOPE
