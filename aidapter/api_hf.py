from . import base

import requests
import json
import os

# TODO: handle error messages

def hf_api_query(payload, model_id, endpoint):
    api_url = f"https://api-inference.huggingface.co/{endpoint}/{model_id}"
    headers = {'Authorization': f'Bearer {os.environ["HF_API_TOKEN"]}'} # TODO
    #
    data = json.dumps(payload)
    raw_resp = requests.request("POST", api_url, headers=headers, data=data)
    resp = json.loads(raw_resp.content.decode("utf-8"))
    return resp

# === TEXT ========================================================================================

class TextModel(base.CompletionModel):

    # TODO
    def transform_one(self, prompt, **kw) -> dict:
        #
        resp = hf_api_query(prompt, self.name, 'models')
        output_text = resp[0]['generated_text'] 
        #
        out = {}
        out['output'] = output_text
        return out

# === EMBEDDING ===================================================================================

# REF: https://huggingface.co/blog/getting-started-with-embeddings
# REF: https://huggingface.co/spaces/mteb/leaderboard

# model_id = 'thenlper/gte-small' # model size: 0.07GB, width: 384
# model_id = 'BAAI/bge-small-en'  # model size: 0.13GB, width: 384

class EmbeddingModel(base.EmbeddingModel):
    def transform_one(self, text, **kw):
        return self.embed_batch([text], **kw)[0]

    def embed_batch(self, texts, **kw):
        limit = kw.get('limit')
        #
        resp = hf_api_query(texts, self.name, 'pipeline/feature-extraction')
        #
        out = []
        for x in resp:
            out.append({
                 'output': x[:limit],
            })
        return out

