# Mamon Utilities

A set of tools and utilities for Python Development

## Installation
```sh
pip install mamon-utils
```

## Usage
To use any of these modules, just import from `mamonutils`.

### Database
This module makes it easy to connect to our PostgreSQL databases. To use it, you have to add a `.env` file in the root of your project specifying the following environment variables:
```.env
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
```

Example usage:
```python
from mamonutils import Database, dotenv

# Load environment variables
dotenv()

# Connect to clients database
db = Database('clients')
cursor = db.cursor

cursor.execute('SELECT * from clients')
result = cursor.fetchall()
print(result)

# Disconnect
db.disconnect()
```