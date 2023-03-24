# This snippet assumes that the lambda has a dynamodb trigger and receives event changes from dynamo
import pandas as pd
import boto3
from boto3.dynamodb.types import TypeDeserializer

deserializer = TypeDeserializer()

def lambda_handler(event, context):
    print("EVENT: ", event)
    for record_index,record in enumerate(event["Records"]):
        key_tmp = record["dynamodb"]["Keys"]
        # Unmarshall Key
        key = {k: deserializer.deserialize(v) for k, v in key_tmp.items()}
        key_val = key["url_key"]
        # Unmarshall data
        data_tmp = record["dynamodb"]["NewImage"]
        data = {k: deserializer.deserialize(v) for k, v in data_tmp.items()}
        
        dyn_df = pd.DataFrame(data, index=[record_index,])
        return dyn_df