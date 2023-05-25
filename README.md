# aidapter

Simple adapter for many language models

## Installation

:construction: This is pre-alpha software. Anything can change without any notice.

```
pip install git+https://github.com/mobarski/aidapter.git
```

## Features

[x] simple API

[x] single interface to many models (remote and local)

[x] parallel calls

[x] caching (when temperature==0)

[x] usage tracking

[x] automatic retries

[  ] logging

[  ] callbacks

[  ] response priming (for older / completion oriented models)



## Usage examples

```python
>>> import aidapter
>>> model = aidapter.model('openai:gpt-3.5-turbo') # uses OPENAI_API_KEY env variable
>>> model.complete('2+2=')
4
>>> model.complete(['2+2=','7*6='])
['4', '42']
>>> model.usage
{'prompt_tokens': 24, 'completion_tokens': 2, 'total_tokens': 26, 'cache_miss': 2, 'cached_prompt_tokens': 12, 'cached_completion_tokens': 1, 'cached_total_tokens': 13, 'cache_hit': 1}
```



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
