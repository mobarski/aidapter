import sys; sys.path[0:0] = ['.','..']

import aidapter

#for model_id in ['transformers:roneneldan/TinyStories-33M']:
#for model_id in ['transformers:TheBloke/guanaco-7B-HF']:
#for model_id in ['transformers:RWKV/rwkv-raven-3b']:
#for model_id in ['transformers:tiiuae/falcon-7b:trust']:
#for model_id in ['transformers:ehartford/Wizard-Vicuna-13B-Uncensored:4bit']:
for model_id in ['transformers:timdettmers/guanaco-33b-merged:4bit']:
    print(f'=== {model_id} ===')
    model = aidapter.model(model_id)
    model.retry_tries = 1
    print(model.complete('there was a little girl who', debug=False))
    print()
    print(model.id)
