import sys
from pyspark.sql import SparkSession

from pyspark.sql.functions import lit
from pyspark.sql import HiveContext

# Variables
qry_filter = sys.argv[1].split('|')
sql_file = qry_filter[0]
schema = qry_filter[1]
table_name = qry_filter[2]
write_mode = qry_filter[3]
partitioned = qry_filter[4]

print("\n\n   sql_file : {}\n\n".format(sql_file))
print("\n\n   schema : {}\n\n".format(schema))
print("\n\n   table_name : {}\n\n".format(table_name))
print("\n\n   write_mode : {}\n\n".format(write_mode))
print("\n\n   partitioned : {}\n\n".format(partitioned))

if partitioned == 'True':
    partition_name = qry_filter[5]
    print("\n\n   partition_name : {}\n\n".format(partition_name))

spark = SparkSession.builder.enableHiveSupport().getOrCreate()
spark.conf.set("hive.exec.dynamic.partition", "true")
spark.conf.set("hive.exec.dynamic.partition.mode", "nonstrict")
spark.conf.set("hive.groupby.orderby.position.alias", "true")

with open(sql_file) as shql:
    file_txt = shql.read()

# Replace schema name in query
# sqlQuery = file_txt.replace('{}',schema)
sqlQuery = file_txt.format(**locals())   # Use locals() (https://docs.python.org/2/library/functions.html#locals) to parse named parameters

print("*** QUERY ***\n", sqlQuery)

#Query hive table
df = HiveContext(spark).sql(sqlQuery)

exportPath='s3://bucketname/{}/{}'.format(schema, table_name)
print("\n\n     Exporting Data to s3 {}:\n\n".format(exportPath))
if partitioned == 'True':
    df.write.partitionBy(partition_name).parquet(exportPath, mode=write_mode, compression='gzip')
else:
    df.write.parquet(exportPath, mode=write_mode, compression='gzip')