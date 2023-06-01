import sys; sys.path[0:0] = ['.','..']
from pprint import pprint

import aidapter

model = aidapter.model('openai:text-embedding-ada-002')
vector = model.embed('hello world', debug=False)
pprint(vector[:5])

vectors = model.embed(['hello','world'])
pprint([x[:5] for x in vectors])

#vectors = model.embed(['hello','world'], debug=True)
#pprint(vectors)

pprint(model.usage)
