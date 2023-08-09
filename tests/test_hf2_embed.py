import sys; sys.path[0:0] = ['.','..']
from pprint import pprint
import diskcache as dc

import aidapter

for model_id in ['huggingface:thenlper/gte-small:embed']:
    model = aidapter.model(model_id)
    model.cache = dc.Cache('/tmp/aidapter/hf')

    pprint( model.embed(['mighty indeed'], limit=5) )
    pprint( model.embed( 'mighty indeed',  limit=5) )

    vectors = model.embed(['this is the way', 'so say we all'], limit=5, cache=False)
    pprint(vectors)

    print('USAGE', model.usage)
