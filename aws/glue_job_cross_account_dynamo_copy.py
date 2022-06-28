# Reference:  https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-dynamo-db-cross-account.html

import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
glue_context= GlueContext(SparkContext.getOrCreate())
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

dyf = glue_context.create_dynamic_frame_from_options(
    connection_type="dynamodb",
    connection_options={
        "dynamodb.region": "us-west-2",
        "dynamodb.input.tableName": "<source_table_name>",
        "dynamodb.sts.roleArn": "<ARN of Role in source account allowing DynamoDB access to target account>"
    }
)
dyf.show()
 
glue_context.write_dynamic_frame_from_options(
    frame=dyf,
    connection_type="dynamodb",
    connection_options={
        "dynamodb.region": "us-west-2",
        "dynamodb.output.tableName": "<source_table_name>"
    }
)

job.commit()
