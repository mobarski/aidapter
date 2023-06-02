import sys; sys.path[0:0] = ['.','..']
from pprint import pprint

import aidapter

model = aidapter.model('sentence-transformers:multi-qa-mpnet-base-dot-v1')
vector = model.embed('mighty indeed')
pprint(vector[:5])

vectors = model.embed(['this is the way', 'so say we all'])
pprint([x[:5] for x in vectors])

#vectors = model.embed(['hello','world'], debug=True)
#pprint(vectors)

pprint(model.usage)
