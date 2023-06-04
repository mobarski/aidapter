from . import base
from sentence_transformers import SentenceTransformer

def use_key(key):
	pass

class EmbeddingModel(base.EmbeddingModel):
    def __init__(self, name, kwargs, options):
        super().__init__(name, kwargs)
        self.model = SentenceTransformer(name)

    def transform_one(self, text, **kw):

        return self.embed_batch([text], **kw)[0]

    def embed_batch(self, texts, **kw):
        limit = kw.get('limit')
        resp = self.model.encode(texts)
        #
        out = []
        for x in resp:
            out.append({'output': list(x)[:limit]})
        return out
