# Cache Toolz
[![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen.svg)](https://gitHub.com/taconi/cachetoolz/graphs/commit-activity)
[![Documentation Status](https://readthedocs.org/projects/cachetoolz/badge/?version=latest)](https://cachetoolz.readthedocs.io/en/latest/?badge=latest)
[![Badge License](https://img.shields.io/github/license/taconi/cachetoolz?label=License&color=%234B78E6)](https://raw.githubusercontent.com/taconi/cachetoolz/main/LICENSE)
![Number of issues](https://img.shields.io/github/issues/taconi/cachetoolz.svg)

[![CI](https://img.shields.io/github/actions/workflow/status/taconi/cachetoolz/tests.yml?branch=main&color=%23FA9BFA&label=tests)](https://github.com/taconi/cachetoolz/actions/workflows/tests.yml)
[![codecov](https://img.shields.io/codecov/c/github/taconi/cachetoolz?style=flat&label=Coverage&color=%2373DC8C)](https://codecov.io/gh/taconi/cachetoolz)
![Repo Size](https://img.shields.io/github/repo-size/taconi/cachetoolz.svg?label=Repo%20size&color=%234B78E6)

[![Supported Python versions](https://img.shields.io/pypi/pyversions/cachetoolz.svg)](https://pypi.python.org/pypi/cachetoolz/)
[![PyPI version](https://badge.fury.io/py/cachetoolz.svg)](https://badge.fury.io/py/cachetoolz)
[![PyBuilder Downloads Per Day](https://img.shields.io/pypi/dd/cachetoolz?logo=pypi)](https://pypi.org/project/cachetoolz/)
[![PyBuilder Downloads Per Week](https://img.shields.io/pypi/dw/cachetoolz?logo=pypi)](https://pypi.org/project/cachetoolz/)
[![PyBuilder Downloads Per Month](https://img.shields.io/pypi/dm/cachetoolz?logo=pypi)](https://pypi.org/project/cachetoolz/)

---

## Usage
```python
from cachetoolz import cache


# Add cache so you don't always have to access the database, for example
@cache(namespace='todo')
async def get_todos(title=None, status=None):
    """Get all todos filtering by title or status."""


# Clear all caches in all namespaces so that no function has the result lagged to the database for example
@cache.clear(namespaces=['todo'])
async def add_todo(title, status=False):
    """Add todo."""
```

## Remote backends

### Redis
```python
from cachetoolz import AsyncRedisBackend, Cache

cache = Cache(AsyncRedisBackend('redis://localhost:6379/0'))


@cache(namespace='todo')
async def get_todos(title=None, status=None):
    """Get all todos filtering by title or status."""


@cache.clear(namespaces=['todo'])
async def add_todo(title, status=False):
    """Add todo."""
```


### Mongo
```python
from cachetoolz import AsyncMongoBackend, Cache

cache = Cache(AsyncMongoBackend('mongodb://username:password@localhost:27017'))


@cache(namespace='todo')
async def get_todos(title=None, status=None):
    """Get all todos filtering by title or status."""


@cache.clear(namespaces=['todo'])
async def add_todo(title, status=False):
    """Add todo."""
```
