import sys; sys.path[0:0] = ['.','..']
from pprint import pprint

import aidapter

model = aidapter.model('openai:text-embedding-ada-002')

vector = model.embed('mighty indeed', limit=5)
pprint(vector)

vectors = model.embed(['this is the way', 'so say we all'], limit=5)
pprint(vectors)

pprint(model.usage)
