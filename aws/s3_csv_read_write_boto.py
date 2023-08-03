import boto3
import io
import os
from io import StringIO
import pandas as pd
import json
import tempfile


s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')

bucketName = "bucket-name"
bucketKey = "parent-dir/child-dir/"
fileKey = bucketKey + "test.csv"

# Read from single file
obj = s3.get_object(Bucket=bucketName, Key=fileKey)
df = pd.read_csv(io.BytesIO(obj['Body'].read()))
df.head()

# write to file
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
s3_resource.Object(bucketName, fileKey).put(Body=csv_buffer.getvalue())

# Read content from all files in an s3 location
bucket = s3_resource.Bucket(bucketName)
bucketObjects = bucket.objects.filter(Prefix=bucketKey)

for obj in bucketObjects:
    objKey = obj.key

    bucketObject = s3_resource.Object(bucket, objKey)
    # get json content
    content = object.get()['Body'].read().decode('utf-8')
    jsonData = json.loads(content)

# Download all files to a temp directory
with tempfile.TemporaryDirectory() as localDir:
    response = s3.list_objects_V2(Bucket=bucketName, Prefix=bucketKey)
    objects = [obj["Key"] for obj in response [ "Contents"]]
    for file in objects:
        localPath = os.path.join(localDir, file.replace(bucketKey, "")) 
        s3.download_file(bucketName, file, localPath)
