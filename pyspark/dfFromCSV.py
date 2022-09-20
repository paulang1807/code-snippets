"""
Code snippet to create a dataframe from a csv file
"""

from pyspark.sql.types import *
from pyspark.sql.functions import *

schema = StructType(
  [
    StructField("col1", StringType(), False),
    StructField("col2", StringType(), False),
    StructField("col3", IntegerType(), False)
  ]
)

fileName = "dir/file.tsv"

# Create DataFrame 
initialDF = (spark.read
  .option("header", "true")
  .option("sep", "\t")    # assume tab delimiter in the csv file
  .schema(schema)
  .csv(fileName)
)

# Alternate approach
df = (spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")  # assuming that the schema is not predefined
    .load("dir/file.csv")
  )