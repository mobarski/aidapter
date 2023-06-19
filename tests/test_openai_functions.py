import sys; sys.path[0:0] = ['.','..']

### 

import aidapter

def get_weather(city):
    "get weather info in a city; city must be all caps after ISO country code and a : separator (e.g. FR:PARIS)"
    pass

model = aidapter.model('openai:gpt-3.5-turbo-0613')
x=model.complete('Whats the weather in the capital of Poland?', functions=[get_weather])
print(x)
# {'function_name': 'get_weather', 'arguments': {'city': 'PL:WARSAW'}}
