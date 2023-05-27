import sys; sys.path[0:0] = ['.','..']

from aidapter.base import BaseModel
import shelve

m = BaseModel('base',{'x':123})
m.cache = shelve.open('/tmp/aidapter-cache.shelve')
m.usage = shelve.open('/tmp/aidapter-usage.shelve')
print(m.complete('hello', stop=['aa','bb'], debug=True))
print(m.complete(range(13)))
print('-'*80)
print(m.complete(range(13)))
print('-'*80)
print(m.complete(range(6), temperature=1.0))
print('-'*80)
print(m.cache)
print('-'*80)
print(dict(m.usage))
