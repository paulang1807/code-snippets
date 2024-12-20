from pyspark.sql.functions import to_date, current_date, date_format
from pyspark.sql.types import DateType
import datetime, time

df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("path/filename.csv")

df2 = df.select(to_date(df.date, 'MM-dd-yyyy').alias('dt'),df.product, df.channel, df.quantity)

min_date, max_date = df2.select(min("dt"), max("dt")).first()
min_date, max_date

df = df.filter(df.dt < datetime(2021,4,1))

# Add current date column
df = df.withColumn("current_date",current_date())

# Cast date col as date
df = df.withColumn("<date_col_name>",df["<date_col_name>"].cast(DateType()))

# Change format
df = df.withColumn("month_year", date_format(df["<date_col_name>"], 'MM-dd'))