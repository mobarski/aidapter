from . import base2 as base

import requests
import json
import os


def hf_api_query(payload, model_id, endpoint):
    api_url = f"https://api-inference.huggingface.co/{endpoint}/{model_id}"
    headers = {'Authorization': f'Bearer {os.environ["HF_API_TOKEN"]}'} # TODO
    #
    data = json.dumps(payload)
    raw_resp = requests.request("POST", api_url, headers=headers, data=data)
    resp = json.loads(raw_resp.content.decode("utf-8"))
    # handle error messages
    if isinstance(resp, dict) and 'error' in resp:
        error = resp['error']
        est_time = resp.get('estimated_time')
        msg = error
        if est_time:
            msg += f' (estimated time: {est_time:0.1f}s)'
        raise ValueError(msg)
    return resp

# === EMBEDDING ===================================================================================

# REF: https://huggingface.co/blog/getting-started-with-embeddings
# REF: https://huggingface.co/spaces/mteb/leaderboard

# model_id = 'thenlper/gte-small' # model size: 0.07GB, width: 384
# model_id = 'BAAI/bge-small-en'  # model size: 0.13GB, width: 384

# TODO: different models -> different output shapes

class EmbeddingModel(base.BaseModelV2):
    brand = 'huggingface'

    def embed(self, inputs, **kwargs):
        return self.transform(inputs, **kwargs)

    def transform_batch(self, inputs, **kwargs):
        limit = kwargs.get('limit')
        resp = hf_api_query(inputs, self.name, 'pipeline/feature-extraction')
        output = [x[:limit] for x in resp]
        self.register_usage({'api-calls':1})
        return output

# === TEXT ========================================================================================

class TextModel(base.BaseModelV2):
    brand = 'huggingface'

    def complete(self, prompts, **kwargs):
        return self.transform(prompts, **kwargs)

    def transform_batch(self, prompts, **kwargs):
        resp = hf_api_query(prompts, self.name, 'models')
        output = [x[0]['generated_text'] for x in resp]
        return output
