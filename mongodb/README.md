# Code Chunks

### Connecting to MongoDB
```python
from pymongo import MongoClient
mongo_host = 'x.x.x.x'    # IP of Mongo Host
mongo_user = 'user_name'
mongo_pass = 'passwd'
mongo_port = 27017
mongo_database = 'db_name'

# Get Mongo Client
mongo_client = MongoClient(mongo_host, mongo_port, username=mongo_user, password=mongo_pass, authSource=mongo_database, connectTimeoutMS=30000, socketTimeoutMS=30000, ssl=False)

# Get Mongo Database
mdb = mongo_client[mongo_database]
```

### Get only specific columns from collection
```python
# Specify required columns in a dictionary within find with Key as the column name and value = 1
m_col = mdb["collection_name"].find({}{"col1":1, "col2":1})
# Convert collection cursor to pandas dataframe
import pandas as pd
df = pd.Dataframe(list(m_col))
```

### Filter collection based on column value
```python
m_col = mdb["collection_name"].find({"col_1": <filter_value_for_col1>, "col_2": <filter_value_for_col2>}{})
# Filter collection and get only specific columns
m_col = mdb["collection_name"].find({"col_1": <filter_value_for_col1>, "col_2": <filter_value_for_col2>}{"col3":1, "col4":1})
```

### Find min and max values of columns
```python
# Min Value
min_val = mdb["collection_name"].find().sort("col_name").limit(1)    # col_name is the column for which min_value is being determined
lst_min_val = list(min_val)
str_min_val = lst_min_val[0]["col_name"]

# Max Value
max_val = mdb["collection_name"].find().sort("col_name", pymongo.DESCENDING).limit(1)    # col_name is the column for which min_value is being determined
lst_max_val = list(max_val)
str_max_val = lst_max_val[0]["col_name"]
```

### Filter data and get count
```python
coll_ct = mdb["collection_name"].aggregate([
  { "$match": { "$and": [{"col_1": <filter_value_for_col1>, "col_2": <filter_value_for_col2>}]}},  # Filter Data
  { "$group": { "_id": None, "count": { "$sum": 1   }}}   # Group and count
])
```

### Filter data and get random sample
```python
m_col = mdb["collection_name"].aggregate([
  { "$match": { "$and": [{"col_1": <filter_value_for_col1>, "col_2": <filter_value_for_col2>}]}},  # Filter Data
  { "$sample": { "size": <sample size> }},   # Specify sample size
  { "$project": {"col1":1, "col2":1}}        # Specify desired columns
])
```