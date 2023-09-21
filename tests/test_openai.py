import sys; sys.path[0:0] = ['.','..']

import aidapter

for model_id in ['openai:gpt-3.5-turbo-instruct','openai:gpt-3.5-turbo']:
    print(f'=== {model_id} ===')
    model = aidapter.model(model_id)
    print(model.complete('2+2='))
    print(model.complete(['2+2=','7*6=']))
    print(model.complete('2+2=', system="answer with words only (don't use numbers)"))
    print(model.complete('2+2=', debug=True))
    print(model.usage)
    print()
