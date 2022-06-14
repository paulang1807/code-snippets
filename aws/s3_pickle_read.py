import pickle
import boto3

# Using boto3 resource
s3 = boto3.resource('s3')
data = pickle.loads(s3.Bucket("bucket-name").Object("key/test.pickle").get()['Body'].read())

# Using boto3 client
s3client = boto3.client('s3')
response = s3client.get_object(Bucket='bucket-name', Key='key/test.pickle')
body = response['Body'].read()
data = pickle.loads(body)