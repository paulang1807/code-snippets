## Code Chunks

### SparkContext and SparkSession
```python
# When using pyspark, sc and spark is available by default as SparkContext and pyspark.sql.session.SparkSession respectively.
# However, when using spark-submit, these will need to be created as follows:
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
sc = SparkContext.getOrCreate()
spark = SparkSession(sc)

# Get rid of unnecessary warning by setting the log level
spark.sparkContext.setLogLevel("ERROR")

# Create a SQL Context
from pyspark.sql import SQLContext
sql_context = SQLContext(sc)
```