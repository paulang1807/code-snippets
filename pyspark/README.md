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

### Cast column as desired datatype
```python
# Cast column as date
df = df.withColumn("datecolname",df["datecolname"].cast(DateType()))
```

### Filter dataframe
```python
from pyspark.sql.functions import col
# Apply multiple filter conditions
df = df.filter(col("col1") == "filterval1").filter(col("col1") != "filterval2")

# Filter one column based on another
df = df.filter(col("<col_to_filter>") <= col("<filter_based_on_col>"))
```

### Set column value conditionally
```python
df = df.withColumn("newColName"), when(df.col1 == x, df.col2 + df.col3).otherwise(df.col2 - df.col3)
```

### Pyspark to Pandas
```python
# Convert Pyspark df to pandas
pd_df = py_df.toPandas()

# Convert Pandas df to Pyspark
py_df = spark.createDataFrame(pd_df)
```