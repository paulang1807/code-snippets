# Sample glue job script for sourcing data from a table
# containing struct columns (with dynamically changing columns)
# flattening the struct columns and populating a target table
# The target table columns will automatically increase or decrease 
# based on changes in the source table

import sys
from awsglue.transforms import *
from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Delete existing files from target table s3 - for truncate and load
glueContext.purge_s3_path("s3://bucket-name/key/", {"retentionPeriod": 0})

# Create Dynamic Frame from source table
DataCatalogtable_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="db-name",
    table_name="source-table-name",
    transformation_ctx="DataCatalogtable_node1",)

# Dataframe from Dynamic Frame
df = DataCatalogtable_node1.toDF()

# Select columns in the struct
df1 = df.select(col("struct_col_name.*"),col("id_col"))

# New dynamic frame by dropping struct field from base Dynamic Frame
dyf1 = DataCatalogtable_node1.drop_fields("struct_col_name", stageThreshold=0, totalThreshold=0)
df2 = dyf1.toDF()   # Dataframe from Dynamic Frame

# Join dataframes
df3 = df2.join(df1,df2.metaKey == df1.metaKey,"inner")
               
# Rename columns (if needed)
df4 = df3.withColumnRenamed("col1name","renamed_col1") \
    .withColumnRenamed("col2name","renamed_col2")
    
# Create Dynamic Frame from Data Frame
dyf2 = DynamicFrame.fromDF(df4, glueContext, "dyf2")

# Write to target table
DataCatalogtable_node3 = glueContext.write_dynamic_frame.from_catalog(
    frame=dyf2,
    database="db-name",
    table_name="tgt-table-name",
    additional_options={
        "enableUpdateCatalog": True,
        "updateBehavior": "UPDATE_IN_DATABASE",
    },
    transformation_ctx="DataCatalogtable_node3",
)

job.commit()
