# Пак "ЮНИор" Python API

## Requiments:
- python: >=3.6
- bleak

## Currently works only with breath sensor!
(maybe will implement other sensor later)

## Usage:
```python
from unior.connection import Connection

connection = Connection('<your mac addr>')

print(connection.value)

connection.disconnect()
```
