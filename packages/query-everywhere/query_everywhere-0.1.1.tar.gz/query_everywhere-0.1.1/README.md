# Query Everywhere

query your data in every RDBMS.

## Notices

* You should install your db driver(like `psycopg2-binary`) before use.

## Example

```python
from query_everywhere import Queryer

# Create a Queryer with DSN
dsn = "sqlite:///test.db"
queryer = Queryer(dsn)


# Query
filters = [
    ("name__contains", "part of name"),
    ("age__gte", 20),
    ("age__lt", 30),
    ("status__in", ["running", "waiting"]),
    ("address__neq", "beijing"),
    ("address__eq", "shanghai"),
    ("address__icontains", "beijing"),
]
order = "create_time desc"
limit = 10
offset = 0
data = queryer.query("users", filters, order, limit, offset)
print(data)
# It where do 
# SELECT * FROM "users" WHERE name LIKE ? AND age >= ? AND age < ? AND status IN ? AND address != ? AND address = ? ORDER BY create_time desc LIMIT 10 OFFSET 0
```

## Supported operators

| Operator | Comment |
| --- | --- |
| eq | equal to |
| neq | not equal to |
| ne | not equal to |
| lt | less than |
| gt | greater than |
| lte | less than or equal to |
| gte | greater than or equal to |
| in | in the list of values |
| startswith | starts with the given value |
| endswith | ends with the given value |
| contains | contains the given value |
| icontains | contains the given value in the case-insensitive way |
