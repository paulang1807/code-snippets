import boto3
import io
import matplotlib.pyplot as plt

bucket_name = 's3_bucket_name'
filepath = 's3_key'

img_data = io.BytesIO()
plt.savefig(img_data, format='png')
img_data.seek(0)  # Set cursor position
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
bucket.put_object(Body=img_data, ContentType='image/png', Key=filepath)
