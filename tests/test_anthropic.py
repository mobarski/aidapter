import sys; sys.path[0:0] = ['.','..']

import aidapter

for model_id in ['anthropic:claude-instant-v1.1']:
    print(f'=== {model_id} ===')
    model = aidapter.model(model_id, temperature=0.1)
    print(model.complete('2+2='))
    print(model.complete(['2+2=','7*6=']))
    print(model.complete('2+2=', system="answer with words only (don't use numbers)"))
    print(model.complete('2+2=', debug=True))
    print(model.usage)
    print()
