import boto3
import os

s3_client = boto3.client('s3')

folder_to_import = 'folder_name'
bucket_name = 's3_bucket_name'

def copyS3DirToLocal(bucketName , local_folder):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketName)
    for obj in bucket.objects.filter(Prefix=f"{folder_to_import}"):
        print (obj)
        if not obj.key.endswith('/'):  # Exclude subdirectories
            # Create the local directory if it doesn't exist
            if not os.path.exists(local_folder):
                os.makedirs(local_folder)
                
            # Create the local path for saving the file
            local_path = os.path.join(local_folder, os.path.basename(obj.key))
            s3_client.download_file(bucketName, obj.key, local_path)
    print("Successfully imported" , f"{folder_to_import}")

# Call the function
copyS3DirToLocal(bucket_name, folder_to_import)
