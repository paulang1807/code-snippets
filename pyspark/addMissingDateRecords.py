"""
Code snippet to modify a dataframe and adding new records for missing dates
Ref: https://stackoverflow.com/questions/46709285/filling-missing-dates-in-spark-dataframe-column
"""
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType
from typing import List
import datetime
# from pyspark.sql import DataFrame, Window
from pyspark.sql.functions import col, lit, udf, datediff, explode, to_timestamp
from pyspark.sql.functions import sum as _sum
from pyspark.sql.types import DateType, ArrayType

# Helper functions for adding dates
def _get_next_dates(start_date: datetime.date, diff: int) -> List[datetime.date]:
    return [start_date + datetime.timedelta(days=days) for days in range(1, diff+1)]

def _get_prev_dates(start_date: datetime.date, diff: int) -> List[datetime.date]:
    return [start_date + datetime.timedelta(days=days) for days in range(diff, 0)]

# Create sample dataframe
schema = StructType([StructField("date", StringType(), True), StructField("product", StringType(), True), StructField("channel", StringType(), True), StructField("quantity", IntegerType(), True)])
df = spark.createDataFrame([("09-10-2016","p1","c1", 1),("09-10-2016","p2","c1", 1),("09-11-2016","p1","c2", 2),("09-14-2016","p2","c2", 0),("09-16-2016","p1","c2", 1),("09-17-2016","p2","c1", 0),("09-20-2016","p1","c2", 2)],schema)

# Convert date column datatype from string to date
df1 = df.select(to_timestamp(df.date, 'MM-dd-yyyy').alias('dt'),df.product, df.channel, df.quantity)

# UDFs
get_next_dates_udf = udf(_get_next_dates, ArrayType(DateType()))
get_prev_dates_udf = udf(_get_prev_dates, ArrayType(DateType()))

# Column Identification
group_columns = ["product","channel"]
date_column = "dt"
fill_column = "quantity"

# Get max and min dates for dataset
max_dt = df1.agg({"dt" :"max"}).collect()[0]
min_dt = df1.agg({"dt" :"min"}).collect()[0]

# Add max and min date columns to dataframe
df2 = df1.withColumn("max_dt", lit(max_dt[0]))
df2 = df2.withColumn("min_dt", lit(min_dt[0]))

# Calculate date difference w.r.t. max and min dates and add columns to dataframe
df3 = df2.withColumn("_diff_max", datediff("max_dt", date_column))
df3 = df3.withColumn("_diff_min", datediff("min_dt", date_column))

# Process data based on max date (where dates greater than the record date are missing)
df4_max = df3.filter(col("_diff_max") > 0)
df5_max = df4_max.withColumn("_next_dates", get_next_dates_udf(date_column, "_diff_max"))

# Process data based on min date (where dates less than the record date are missing)
df4_min = df3.filter(col("_diff_min") < 0)
df5_min = df4_min.withColumn("_next_dates", get_prev_dates_udf(date_column, "_diff_min"))

#  Combine dataframes for all missing data
df5 = df5_max.union(df5_min)

# Add dummy value
df6 = df5.withColumn(fill_column, lit(0))

# Explode dates
df7 = df6.withColumn(date_column, explode("_next_dates"))

# Drop columns that were added for processing
df8 = df7.drop("max_dt", "min_dt","_diff_max", "_diff_min", "_next_dates")

# Drop duplicates
df9 = df8.dropDuplicates()

# Combine with base dataframe
df10 = df9.union(df1)
df10.dropDuplicates()

# Aggregate to get rid of rows from the exploded data that are already present in the base dataframe
df11 = df10.groupBy("dt","product","channel").agg(_sum("quantity"))

df11.sort("dt").show(10)