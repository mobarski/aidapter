import sys; sys.path[0:0] = ['.','..']
from pprint import pprint

import aidapter

model = aidapter.model('hf:thenlper/gte-small:embed')

vector = model.embed('mighty indeed', limit=5)
pprint(vector)

vectors = model.embed(['this is the way', 'so say we all'], limit=5)
pprint(vectors)

pprint(model.usage)


model = aidapter.model('hf:gpt2')
print(model.complete(['2+2=']))
print(model.complete(['2+2=','7*6=']))
