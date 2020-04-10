import boto3
import io
from io import StringIO
import pandas as pd

# Read from file
s3 = boto3.client('s3')
bucket = 'crpfin-oip-prd'
key = 'temp/oip-meta/oif_meta.csv'

obj = s3.get_object(Bucket=bucket, Key=key)
df = pd.read_csv(io.BytesIO(obj['Body'].read()))
df.head()

# write to file
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
s3_resource = boto3.resource('s3')
s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())