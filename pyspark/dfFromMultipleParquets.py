"""
Code snippet to create a dataframe from a directory containing multiple parquet files
"""

import re
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

spark = SparkSession.builder.enableHiveSupport().getOrCreate()

# Define Schema
customSchema = StructType([
    StructField("field1", StringType(), True),
    StructField("field2", DoubleType(), True),
    StructField("field3", IntegerType(), True),])

# Create empty dataframe
df = spark.createDataFrame(spark.sparkContext.emptyRDD(),customSchema)
df.printSchema()

hfolder = '/tmp/data/'   # hdfs folder
lfolder = '/w205/data'   # local folder
for file in os.listdir(lfolder):
    # Create temporary dataframe for each parquet file
    df_temp = sqlContext.read.format("parquet").\
        schema(customSchema). \
        load(hfolder + file)
    
    # Union with the original dataframe
    df = df.union(df_temp)

df.count()