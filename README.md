# aidapter

Simple adapter for many language models -  remote (OpenAI, AnthropicAI, CohereAI) and local (transformers library).

Facilitates loading of many new models (Guanaco, Falcon, RWKV, Vicuna, etc) in 16/8/4 bit modes.

## Installation

:construction: This is pre-alpha software. Anything can change without any notice.

```
pip install git+https://github.com/mobarski/aidapter.git
```

**Note**: each vendor API requires manual installation of dependencies.

## Features

- simple API interface to many models (remote and local)
- parallel calls
- caching
- usage tracking
- automatic retries
- ~~logging~~
- ~~callbacks~~
- ~~response priming (for older / completion oriented models)~~



## Usage examples

```python
>>> import aidapter
>>> model = aidapter.model('openai:gpt-3.5-turbo') # uses OPENAI_API_KEY env variable
>>> model.complete('2+2=')
4
>>> model.complete(['2+2=','7*6=']) # parallel
['4', '42']
```

```python
>>> model.usage
{'prompt_tokens': 24, 'completion_tokens': 2, 'total_tokens': 26, 'cache_miss': 2, 'cached_prompt_tokens': 12, 'cached_completion_tokens': 1, 'cached_total_tokens': 13, 'cache_hit': 1}
```

```python
>>> import shelve
>>> model.cache = shelve.open('/tmp/aidapter.cache') # persistant disk cache
>>> model.usage = shelve.open('/tmp/aidapter.usage') # persistant usage tracking (total and daily, can be customised)
```



## Supported models

### OpenAI

- `openai:gpt-4`
- `openai:gpt-4-32k`

- `openai:gpt-3.5-turbo`

- `openai:text-davinci-003`
- `openai:code-davinci-002`
- ...

API key env. variable: **OPENAI_API_KEY**

### Anthropic

- `anthropic:claude-v1`

- `anthropic:claude-instant-v1`

- `anthropic:claude-v1-100k`

- `anthropic:claude-instant-v1-100k`
- ...

API key env. variable: **ANTHROPIC_API_KEY**

### Cohere

- `cohere:command`

- `cohere:command-light`
- ...

API key env. variable: **CO_API_KEY**

### Transformers

- `transformers:TheBloke/guanaco-7B-HF`
- `transformers:tiiuae/falcon-7b`
- `transformers:RWKV/rwkv-raven-3b`
- `transformers:ehartford/Wizard-Vicuna-13B-Uncensored`
- `transformers:roneneldan/TinyStories-33M`
- ...



## API



**aidapter.model**(model_id, \*\*api_kwargs) **-> model**

- `model_id` - model identifier in the following format `<vendor_name>:<model_name>`
- `api_kwargs` - default API arguments



**model.complete**(prompt, system='', stop=[], limit=100, temperature=0, debug=False) **-> str | list | dict**

- `prompt` - main prompt or list of prompts

- `system` - system prompt

- `stop` - list of strings upon which to stop generating

- `limit` - maximum number of tokens to generate before stopping (aka max_new_tokens, max_tokens_to_sample)

- `temperature` - amount of randomness
- `debug` - if True, the function will return a dictionary (or a list of dictionaries) containing internal objects / values



**model configuration:**

- `model.workers` - number of concurrent workers for parallel completion (default=4)

- `model.show_progress` - show progress bar when performing parallel completion (default=False)

- `model.retry_tries` - maximum number of retry attempts (default=5)

- `model.retry_delay` - initial delay between retry attempts (default=0.1)

- `model.retry_backoff` - multiplier applied to the delay between retry attempts (default=3)





## Change log

### 0.4.1

- remove prompt from transformers output

### 0.4

- initial support for local transformers models

  - float16 (add ":16bit" to the model name)

  - load_in_8bit (add ":8bit" to the model name)

  - load_in_4bit (add ":4bit" to the model name)

- cache = use | skip | force

- shelve based persistence (for cache and usage)

### 0.3.2

- kvdb import fix

### 0.3

- Cohere models
- disk cache

### 0.2

- OpenAI instruct models
- Anthropic models (ANTHROPIC_API_KEY env variable)
- complete: debug option
- BaseModel.RENAME_KWARGS
- pip install
- limit handling

### 0.1

- parallel calls / cache / usage tracking / retries
- OpenAI chat models



## Related projects

- https://github.com/kagisearch/pyllms

