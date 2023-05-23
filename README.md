# aidapter

Simple adapter for many language models

## Installation

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

[  ] response priming (great for older / completion oriented models)

[  ] logging

[  ] callbacks



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



## Changelog

0.1 - MVP:

- parallel calls / cache / usage tracking / retries
- OpenAI chat models
