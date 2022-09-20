""" 
Code snippet to create a pyspark dataframe manually
and convert a date column from string to date data type

class pyspark.sql.types.StructField(name: str, dataType: pyspark.sql.types.DataType, nullable: bool = True, metadata: Optional[Dict[str, Any]] = None)
"""

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType
from pyspark.sql.functions import to_timestamp

schema = StructType([StructField("date", StringType(), True), StructField("product", StringType(), True), StructField("channel", StringType(), True), StructField("quantity", IntegerType(), True)])

df = spark.createDataFrame([("09-10-2016","p1","c1", 1),("09-10-2016","p2","c1", 1),("09-11-2016","p1","c2", 2),("09-14-2016","p2","c2", 0),("09-16-2016","p1","c2", 1),("09-17-2016","p2","c1", 0),("09-20-2016","p1","c2", 2)],schema)

df.printSchema()

df2 = df.select(to_timestamp(df.date, 'MM-dd-yyyy').alias('dt'),df.product, df.channel, df.quantity)

df2.printSchema()