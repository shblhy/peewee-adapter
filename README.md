Peewee Adapter for PyCasbin
====

[![Build Status](https://www.travis-ci.org/shblhy/peewee-adapter.svg?branch=master)](https://www.travis-ci.org/shblhy/peewee-adapter)
[![Coverage Status](https://coveralls.io/repos/github/shblhy/peewee-adapter/badge.svg)](https://coveralls.io/github/shblhy/peewee-adapter)
[![Version](https://img.shields.io/pypi/v/casbin_peewee_adapter.svg)](https://pypi.org/project/casbin_peewee_adapter/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/casbin_peewee_adapter.svg)](https://pypi.org/project/casbin_peewee_adapter/)
[![Pyversions](https://img.shields.io/pypi/pyversions/casbin_peewee_adapter.svg)](https://pypi.org/project/casbin_peewee_adapter/)
[![Download](https://img.shields.io/pypi/dm/casbin_peewee_adapter.svg)](https://pypi.org/project/casbin_peewee_adapter/)
[![License](https://img.shields.io/pypi/l/casbin_peewee_adapter.svg)](https://pypi.org/project/casbin_peewee_adapter/)

Peewee Adapter is the [Peewee](http://docs.peewee-orm.com/en/latest/) adapter for [PyCasbin](https://github.com/casbin/pycasbin). With this library, Casbin can load policy from Peewee supported database or save policy to it.

Based on [Officially Supported Databases](http://docs.peewee-orm.com/en/latest/), The current supported databases are:

- PostgreSQL
- MySQL
- SQLite

## Installation

```
pip install casbin_peewee_adapter
```

## Simple Example

```python
import casbin_peewee_adapter
import casbin
import peewee
DATABAEE = peewee.SqliteDatabase('db.sqlite3')
adapter = casbin_peewee_adapter.Adapter(database=DATABAEE)

e = casbin.Enforcer('path/to/model.conf', adapter, True)

sub = "alice"  # the user that wants to access a resource.
obj = "data1"  # the resource that is going to be accessed.
act = "read"  # the operation that the user performs on the resource.

if e.enforce(sub, obj, act):
    # permit alice to read data1casbin_peewee_adapter
    pass
else:
    # deny the request, show an error
    pass
```


### Getting Help

- [PyCasbin](https://github.com/casbin/pycasbin)

### License

This project is licensed under the [Apache 2.0 license](LICENSE).
