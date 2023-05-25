from kvdb import KV

def model(model_id, **kwargs):
	brand,_,name = model_id.partition(':')
	if brand=='anthropic':
		from . import api_anthropic
		return api_anthropic.ChatModel(name, kwargs)
	elif brand=='openai':
		from . import api_openai
		if name.startswith('gpt-'):
			return api_openai.ChatModel(name, kwargs)
		else:
			return api_openai.TextModel(name, kwargs)
	elif brand=='cohere':
		from . import api_cohere
		return api_cohere.TextModel(name, kwargs)
	elif brand=='huggingface':
		pass
