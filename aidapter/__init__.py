def model(model_id, **kwargs):
	brand,_,name = model_id.partition(':')
	if brand=='anthropic':
		from . import api_anthropic
		return api_anthropic.ChatModel(name, kwargs)
	elif brand=='openai':
		if name.startswith('gpt-'):
			from . import api_openai
			return api_openai.ChatModel(name, kwargs)
		else:
			from . import api_openai
			return api_openai.TextModel(name, kwargs)
	elif brand=='huggingface':
		pass
