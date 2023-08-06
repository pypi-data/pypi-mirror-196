# yet-another-json-config
Python class to reads and write json files as a configuration file, supports nested json values.

# Examples

## Initializing Config
```py
from yet_another_json_config import Config

c = Config('./tests/test.json')
```

## Listing Settings
```py
from yet_another_json_config import Config

c = Config('./tests/test.json')

print(c.settings)
```

### Output
```json
{
    "test": "test",
    "varUserTest": "test_$user$",
    "nestedTest": {
        "test": "test"
    },
    "nestedTest2": {
        "nested": {
            "test": "test"
        }
    },
    "get": "test"
}
```

## Get Setting
Settings can be obtained two ways through the method `get`

### Class Method `get`
```py
# setting a basic setting
c.get('test')

# setting a nested setting via list of strings
c.get('nestedTest2', 'nested', 'test')

# setting a nested setting via tuple
c.get(('nestedTest2', 'nested', 'test'))
```

### `key` Method
```py
# setting a basic setting
print(c['test'])

# setting a nested setting
print(c['nestedTest2']['nested']['test'])
```

## Set Setting
Settings can be both created and modified using the same methods. If a setting does not exist and one of the following methods is used, it will be created. If the setting already exists, it will be updated.

### Class Method `set`
This method supports *args for defining the keys for a setting. This means that a list of strings (not type of list) or a tuple can be passed to set the value.

```py
# setting a basic setting
c.set('test', value='test2')

# setting a nested setting via list of strings
c.set('nestedTest2', 'nested', 'test', value='test2')

# setting a nested setting via tuple
c.set(('nestedTest2', 'nested', 'test'), value='test2')
```

### `key` Method
```py
# setting a basic setting
c['test'] = 'test2'

# setting a nested setting
c['nestedTest2']['nested']['test'] = 'test2'
```

## Delete Setting
Settings can be deleted two ways through the method `delete` and the `del` statement. As well, nested settings can also be deleted. Below are an example of each.

### Class Method `delete`
```py
# deleting a basic setting
c.delete('test')

# deleting a nested setting
c.delete(('nestedTest2', 'nested', 'test'))
```

### `del` Statement Method
```py
# deleting a basic setting
del c['test']

# deleting a nested setting
del c['nestedTest2']['nested']['test']
```