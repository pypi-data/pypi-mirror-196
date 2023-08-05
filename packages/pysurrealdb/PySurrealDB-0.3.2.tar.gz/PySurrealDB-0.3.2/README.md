# PySurrealDB

[![Join the chat at https://gitter.im/pysurrealdb/community](https://badges.gitter.im/pysurrealdb/community.svg)](https://gitter.im/pysurrealdb/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

An unofficial library to connect to SurrealDB.

Minimal dependencies, easy to use.

---
## Getting Started

If you don't already have it, install [SurrealDB](https://surrealdb.com/docs/start/installation)

Linux: 
``` bash
$ curl -sSf https://install.surrealdb.com | sh
# then
$ surreal start --user test --pass test
```


### Install PySurrealDB
```
pip install pysurrealdb
```


### Examples

```python
import pysurrealdb as surreal

conn = surreal.connect(user='test', password='test')

conn.create('person', {'name': 'Mike'})
conn.query('select * from person')
```

You can specify additional connection info either in the connect call, or in a config file.

```python
import pysurrealdb as surreal
conn = surreal.connect(host='surreal.com', port=8000, user='user', password='pass', database='db', namespace='ns')
```

Both http and websocket are supported. Specify which to use with the client keyword.
```python
conn = surreal.connect(client='websocket')
# Websocket was added and made the default as of version 0.3. Try http if you run into issues, and please report any bugs you find!
```

Optional Config file:
```python
# use a configured connection. 
conn = surreal.connection('default')
# Requires pysurrealdb.json file. Place it in your root directory, or specify the file location with the env variable 'PYSURREALDB_CONFIG'.

Example pysurrealdb.json:
{
    "connections": {
        "default": {
            "host": "localhost",
            "port": 8000,
            "user": "test",
            "password": "test"
            "database": "test",
            "namespace": "test",
            "client": "http",
        }
    }
}

# when using a config file, you do not even need to connect, you can access most functions directly:
import pysurrealdb as surreal

surreal.query('select * from test') # uses the last connection from connect() or the default connection if connect() has not been called.
```


## Query Builder

You can write queries using Laravel and Orator style syntax:
```python
import pysurrealdb as surreal
conn = surreal.connection()

# setup data
conn.drop('person')
conn.insert('person', [{'name': 'Mike', 'age': 31}, {'name':'Mr P'}])

# query builder examples
first_person = conn.table('person').where('name', 'Mike').first()

adults = conn.table('person').where('age', '>=', 18).order_by('age', 'desc').limit(10).get()
```

## Methods
Some of the basic methods available:
```python
query(sql)
get(table, id='')
insert(table, data)
create(table, data)
update(table, data)
upsert(table, data)
delete(table, id)
drop(table)
relate(noun, verb, noun2, data={})

# Most methods accept a table or table:id as the main arguement. The data is also checked for an ID when relevant.
```


This project is a work in progress. Questions and feedback are welcome! Please create an issue or use the gitter chat link at the top. Thanks!
