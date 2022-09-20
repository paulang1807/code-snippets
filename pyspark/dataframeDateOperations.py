from pyspark.sql.functions import to_date
import datetime, time

df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("path/filename.csv")

df2 = df.select(to_date(df.date, 'MM-dd-yyyy').alias('dt'),df.product, df.channel, df.quantity)

min_date, max_date = df2.select(min("dt"), max("dt")).first()
min_date, max_date

df = df.filter(df.dt < datetime(2021,4,1))