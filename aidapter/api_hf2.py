#from . import base2 as base
import base2 as base

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
    embed = base.BaseModelV2.transform

    def transform_batch(self, inputs, **kwargs):
        limit = kwargs.get('limit')
        resp = hf_api_query(inputs, self.name, 'pipeline/feature-extraction')
        output = [x[:limit] for x in resp]
        self.register_usage({'api-calls':1})
        return output

# === TEXT ========================================================================================

class TextModel(base.BaseModelV2):
    brand = 'huggingface'
    complete = generate = base.BaseModelV2.transform

    def transform_batch(self, prompts, **kwargs):
        resp = hf_api_query(prompts, self.name, 'models')
        try:
            output = [x[0]['generated_text'] for x in resp]
        except KeyError:
            output = [x['generated_text'] for x in resp]
        return output

if __name__=="__main__":
    #model_id = 'Voicelab/vlt5-base-keywords'
    #model_id = 'bloomberg/KeyBART'
    model_id = 'ml6team/keyphrase-generation-t5-small-inspec'
    print(hf_api_query(['this is example text about space and space-exploration','underwater light propagation in antarctica'], model_id, 'models'))
    model = TextModel(model_id, {},{})
    print(model.generate(['this is example text about space and space-exploration','underwater light propagation in antarctica']))
