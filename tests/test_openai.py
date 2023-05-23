import sys; sys.path[0:0] = ['.','..']

import aidapter

model = aidapter.model('openai:gpt-3.5-turbo')
print(model.complete('2+2='))
print(model.complete(['2+2=','7*6=']))
print(model.usage)
