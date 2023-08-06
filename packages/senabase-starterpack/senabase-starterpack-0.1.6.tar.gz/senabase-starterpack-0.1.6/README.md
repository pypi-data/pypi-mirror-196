# senabase-starterpack

senabase-starterpack is personal library for fast prototyping.

## Installation

Use `pip` to download it from [PyPI](https://pypi.org/project/senabase-starterpack/)

```shell
$ pip install senabase-starterpack
```

The minimum required versions of the respective tools are:

```
psycopg2-binary>=2.9.*
pyyaml>=6.*
```

## Example

### PostgreSQLHandler

Postgresql starterpack

```python
from senabase.starterpack.database import PostgreSQLHandler

pgh = PostgreSQLHandler()
pgh.configure('127.0.0.1', 5432, 'postgres', 'userid', 'userpassword')

q1 = 'select now()'
rs = pgh.get(q1)
```

### log

Logging starterpack

```python
from senabase.starterpack.log import SimpleLogger

log = SimpleLogger()
log.configure('proto')

log.i('Information')
log.d('Debug')
log.e(Exception('Example exception'))
```