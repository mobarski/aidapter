import sys; sys.path[0:0] = ['.','..']

import aidapter

for model_id in ['cohere:command-light']:
    print(f'=== {model_id} ===')
    model = aidapter.model(model_id)
    model.retry_tries = 1
    print(model.complete('2+2='))
    print(model.complete(['2+2=','7*6=']))
    print(model.complete('2+2=', system="answer with words only (don't use numbers)"))
    print(model.complete('2+2=', debug=True))
    print(model.usage)
    print()
