import sys; sys.path[0:0] = ['.','..']
import aidapter

model_id = 'transformers:RWKV/rwkv-raven-3b'
#model_id = 'openai:text-davinci-003'
#model_id = 'openai:gpt-3.5-turbo'
#model_id = 'anthropic:claude-v1'
#model_id = 'cohere:command-light'

model = aidapter.model(model_id)

print('===')
print(model.complete('Alice: Hello, my name is Alice.\nBob:'))

print('===')
print(model.complete('Alice: Hello, my name is Alice.\n', start='Bob:'))

print('===')
print(model.complete('Alice: Hello, my name is Alice.\n', start='Bob:', stop=['Alice:','.']))
