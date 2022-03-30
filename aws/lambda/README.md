## Create Lambda Layer for Python packages

### References
- [Lambda template](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html)
- [Creating package zip file](https://aws.amazon.com/premiumsupport/knowledge-center/lambda-layer-simulated-docker/)
- [Third Party for prepackaged layers](https://github.com/keithrozario/Klayers/blob/master/deployments/python3.8/arns/us-west-2.csv)

### Steps
- Create a folder
- Create the requirements.txt file in the folder specifying the python packages to be added to the layer
- Requirements.txt file content sample:
  ```
  pytz==2018.9
  s3fs==0.3.4
  pandas==0.22.0
  ```
- Run the following command in the terminal
  ```shell
  docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.8" /bin/sh -c "pip install -r requirements.txt -t python/lib/python3.8/site-packages/; exit"
  ```
  - This will create a folder and add the output of the `pip install` command in the folder.
- Zip the folder created above
  ```shell
  zip -r <zip_file_name>.zip python > /dev/null
  ```
-Upload the zip file to s3
- Create a `CloudFormation` template (layer.yml) for creating the layer in aws. Sample template:
  ```yml
  AWSTemplateFormatVersion: '2010-09-09'
  Transform: AWS::Serverless-2016-10-31
  Description: Lambda Layers Test

  Resources:
    MyLayer:
      Type: AWS::Lambda::LayerVersion
      Properties:
        CompatibleRuntimes:
          - python3.6
          - python3.7
          - python3.8
        CompatibleArchitectures:
          - x86_64
        Content:
          S3Bucket: bucket-name
          S3Key: <s3_key>/<zip_file_name>.zip
        Description: My python package layer
        LayerName: my-python-package-layer
        LicenseInfo: MIT
  ```
- Execute the following `SAM Cli` commands to build and deploy the layer in aws:
  ```aws
  sam build -t layer.yaml --use-container

  sam deploy --stack-name lambda-layer-test --s3-bucket bucket-name --region us-west-2 --capabilities CAPABILITY_NAMED_IAM
  ```