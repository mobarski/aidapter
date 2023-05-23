def model(model_id, **kwargs):
	brand,_,name = model_id.partition(':')
	if brand=='anthropic':
		pass
	elif brand=='openai':
		if name.startswith('gpt-'):
			from . import api_openai
			return api_openai.ChatModel(name, kwargs)
	elif brand=='huggingface':
		pass
