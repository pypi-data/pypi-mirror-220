# flexible_dict: simple way to handle json format data in python

## example

```python
from flexible_dict import json_object, MISSING

@json_object
class A:
    i: int = 3
    j: str = "init value"
    s: float
    g: int = MISSING

a = A()
print(a)  # actual is a dict

print(a.i)  # access value via x.y
print(a.j)

a.j = "update value"  # set value

print(a['j'])  # access value via native dict way
```
