# a3faker

* It's just a thin wrapper of [Faker](https://pypi.org/project/Faker/), because PyCharm cannot autocomplete Faker related code.

## Install

```shell script
pip install a3faker

```

## Examples

### 1. Autocomplete

```python
from faker import Faker
from a3faker import TypePersonFaker, TypeAllFakers

# But there is a warning here，the solution is below.
f: TypePersonFaker = Faker()
f.name()

f: TypeAllFakers = Faker()
f.past_date()

```

### 2. `FakerProxy` get LOCALE from environment variable


```python
import os
from a3faker import FakerProxy, TypePersonFaker

os.environ['FAKER_LOCALE'] = 'zh_CN'
f: TypePersonFaker = FakerProxy.get_faker()
f.name()

```
