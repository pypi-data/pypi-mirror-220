# hdb
Persistent, hobbit-sized dictionaries

## Example Usage
```python
import os
import hdb

# Create a hobbit dictionary at location `pack`.
pack = hdb.get('pack')

# Set a key value pair.
pack['food'] = 'lembas'

# Persist the dictionary to disk.
pack.save()

# Confirm that the dictionary was saved.
# The `location` specifies the path on disk.
print(pack.location)
print(os.path.abspath(pack.location))
print(os.path.exists(pack.location))
```

We can later retrieve the dictionary like so:
```python
import hdb

new_session = hdb.get('pack')
print(new_session)

# We can then further edit the data, and store it to the same location.
new_session['supplies'] = 'taters'
new_session.save()
```
