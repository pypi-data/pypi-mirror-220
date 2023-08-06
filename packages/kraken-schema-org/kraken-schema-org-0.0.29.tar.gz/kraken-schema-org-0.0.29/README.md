Library to schema_org

Provides functions to normalize @type, keys/attributes and values following schema.org notation


# How to use:

```
from kraken_schema_org import kraken_schema_org as k
```

## Normalize @type
```
record_type = 'person'
normalized_type = k.normalize_type(record_type)
```

## Normalize key/attribute
```
key = 'givenname'
normalized_key = k.normalize_key(key)
```

## Normalize value or record

```
record = {"@type": "schema:WebPage", "schema:url": "https://www.test.com"}
normalized_record = k.normalize_record(record)
normalized_value = k.normalize_value(record_type: str, key: str, value: xx, strict: bool)

```

## Get keys/attributes for a given @type

```
record_type = 'person'
keys = k.get_keys(record_type)
```

## Get Datatypes for a given key

```
record_type = 'schema:Person'
key = 'schema:givenName'
datatypes = k.get_datatype(record_type, key)
```

