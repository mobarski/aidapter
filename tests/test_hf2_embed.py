import sys; sys.path[0:0] = ['.','..']
from pprint import pprint

import aidapter

#for model_id in ['hf:BAAI/bge-large-en']:
for model_id in ['hf2:thenlper/gte-small:embed','hf:thenlper/gte-small:embed']:
    model = aidapter.model(model_id)

    pprint( model.embed(['mighty indeed'], limit=5) )
    pprint( model.embed( 'mighty indeed',  limit=5) ) # ERROR -> each char as prompt

    vectors = model.embed(['this is the way', 'so say we all'], limit=5)
    pprint(vectors)

    print(model.usage)

#model = aidapter.model('hf:gpt2')
#print(model.complete(['2+2=']))
#print(model.complete(['2+2=','7*6=']))
