import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Create Dynamic Frame from source table
DataCatalogtable_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="db-name",
    table_name="source-table-name",
    transformation_ctx="Ctx_node1",)

# Map source to target columns
ApplyMapping_node2 = ApplyMapping.apply(
    frame=DataCatalogtable_node1,
    mappings=[
        ("src-col-1", "src-col-1-datatype", "tgt-col-1", "tgt-col-1-datatype"),
        ("src-col-2", "src-col-2-datatype", "tgt-col-2", "tgt-col-2-datatype"),
        ...
        ("src-col-n", "src-col-n-datatype", "tgt-col-n", "tgt-col-n-datatype"),
    ],
    transformation_ctx="ApplyMapping_node2",
)

# Write to target table
DataCatalogtable_node3 = glueContext.write_dynamic_frame.from_catalog(
    frame=ApplyMapping_node2,
    database="db-name",
    table_name="tgt-table-name",
    transformation_ctx="DataCatalogtable_node3",
)

job.commit()