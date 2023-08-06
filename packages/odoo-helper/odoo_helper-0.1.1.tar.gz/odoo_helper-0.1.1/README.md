# odoo_python - Database

This package will help to connect odoo database. It converts ``xmlrpc`` based api into into simple functions.

Please give it a star on github if you like it.

[github repo](https://github.com/dharmendrasha/odoo_python)

[Dharmendra Soni](https://github.com/dharmendrasha)

## How to install

```bash
pip install odoo-helper
```

## How to use

```python
from odoo_helper import api
```

## Initialize it

```python
odoo = api(
    self.url = 'host'
    self.db = 'database'
    self.user = 'user'
    self.password = 'password'
)
```

## Get a version

```python
odoo.version() # 1.1
```

## Get a Client

```python
odoo.client() # xmlrpc.client
```

## Get a authenticate

```python
odoo.authenticate() # boolean
```

## Check access to a certain model

```python
odoo.check_access(
    model: str,
    right: str = 'check_access_rights',
    chmod: List[str] = ['read'],
    raise_exception: bool = True,
) # boolean
```

## search record in the model

```python
odoo.search(
    model: str,
     condition: List[List[list]] = [[]], 
     limit: int = -1, 
     offset: int = -1
     ) # any
```

## search record in the model and returns their ids

```python
odoo.search(
    model: str,
     condition: List[List[list]] = [[]], 
     limit: int = -1, 
     offset: int = -1
     ) # any
```

## read record in the model and returns their row

```python
odoo.records(
    model: str,
     condition: List[List[list]] = [[]], 
     limit: int = -1, 
     offset: int = -1
     ) # any
```

## count record in the model

```python
odoo.count_records(
    model: str, 
    condition: List[List[list]] = [[]]
    ): # any
```

## check if data exists or not

```python
odoo.fields_get(
    model: str, 
    condition: List[List[list]] = [[]], 
    attributes: List[str] = []
    ): # any
```

## search the table and fetch the records from model

```python
odoo.fields_get(
    self, model: str, 
    condition: List[List[list]] = [[]], 
    fields: List[str] = [], 
    limit: int = -1,
    offset: int = -1
    ): # any
```

## creates a records

```python
odoo.create(
    model: str, 
    data: list = []
    ): # any
```

## updates a records

```python
odoo.update(
    model: str, 
    id: List[int], 
    value: dict
    ):
```

## delete a records

```python
odoo.delete(
   model: str, 
   condtion: List[List[list]] = [[]]
    ):
```
