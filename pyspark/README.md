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

### SparkSession with Hive Support enabled
```python
SparkSession = (
    SparkSession.builder
        .enableHiveSupport()
        .getOrCreate())
```

### Create SparkSession locally
```python
from pyspark.sql import SparkSession

# Create SparkSession locally with 'X' number of worker threads
appName = "Test app"
master = "local[X]"

spark = SparkSession.builder \
    .appName(appName) \
    .master(master) \
    .getOrCreate()
```

### Add columns to dataframe
```python
# Assuming we have an existing dataframe with a date column, we can add columns for day, month, year etc. as shown below
df = df.withColumn("Year", year("Date")).withColumn(
"Month", month("Date")).withColumn("Day", dayofmonth("Date"))
```