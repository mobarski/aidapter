
def model(model_id, **kwargs):
	"model factory function"
	brand,_,name = model_id.partition(':')
	name,_,options = name.partition(':')
	#
	if brand=='anthropic':
		from . import api_anthropic
		model =  api_anthropic.ChatModel(name, kwargs)
	elif brand=='openai':
		from . import api_openai
		if name.startswith('gpt-'):
			model = api_openai.ChatModel(name, kwargs)
		elif 'embedding' in name:
			model = api_openai.EmbeddingModel(name, kwargs)
		else:
			model = api_openai.TextModel(name, kwargs)
	elif brand=='cohere':
		from . import api_cohere
		if 'embed' in name:
			model = api_cohere.EmbeddingModel(name, kwargs)
		else:
			model = api_cohere.TextModel(name, kwargs)
	elif brand=='transformers':
		from . import api_transformers
		model = api_transformers.TextModel(name, kwargs, options)
	elif brand=='sentence-transformers':
		from . import api_sentence_transformers
		model = api_sentence_transformers.EmbeddingModel(name, kwargs, options)
	else:
		raise ValueError(f'unknown brand: {brand}')
	#
	model.id = model_id
	model.id_safe = model_id.replace('/','--')
	return model
