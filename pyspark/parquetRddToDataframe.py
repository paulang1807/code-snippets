"""
Code snippet to read parquet files into a RDD and then convert the RDD to a dataframe
"""

from pyspark.sql.types import *
from pyspark.sql.functions import *

testRDD = sc.textFile("dir/parquet_file_path")

df = testRDD.map(lambda x: x.split(",")).toDF(["col1","col2","col3"])  # the data has 3 columns