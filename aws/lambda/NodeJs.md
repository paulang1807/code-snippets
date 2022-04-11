## Create Lambda Function for Node Js Code

### References
- [AWS Guide (Git)](https://github.com/awsdocs/aws-lambda-developer-guide/tree/main/sample-apps/blank-nodejs)

### Steps
- Create a folder
- Create a subfolder called `src` within this folder. The node code will be created in this subfolder (the index js in the subfolder location will be used to specify the `Handler` property in the CloudFormation template).
- Create the `index.js` file
  ```javascript
  <!-- Sample Code -->
  const enigma = require('dotenv');  // require packages

  exports.handler = async (event) => {
      let msg = 'Hello from Lambda';

      exports.handler = async (event) => {
        let msg = 'Hello from Lambda';
        console.log("message: ", msg);
        return msg;
      };

  ```
- Create a shell script (layer.sh) for building a layer with the desired npm packages
  ```bash
  #!/bin/bash
  set -eo pipefail
  mkdir -p lib/nodejs
  rm -rf node_modules lib/nodejs/node_modules
  npm install <package1> <package2> <...>
  mv node_modules lib/nodejs/
  ```
- Run the script to move the node modules to the `lib` folder (the `lib` folder create will be used to specify the `LayerName` property in the CloudFormation template)
  ```bash
  ./layer.sh
  ```
- Create a `CloudFormation` template (layer.yml) for creating the layer in aws. Sample template:
  ```yml
  AWSTemplateFormatVersion: '2010-09-09'
  Transform: 'AWS::Serverless-2016-10-31'
  Description: An AWS Lambda node hello world application.
  Resources:
    function:
      Type: AWS::Serverless::Function
      Properties:
        Handler: src/index.handler
        Runtime: nodejs12.x
        CodeUri: function/.
        Description: Call the AWS Lambda API
        Timeout: 10
        # Function's execution role
        Role: <role_arn>
        Tracing: Active
        Layers:
          - !Ref libs
    libs:
      Type: AWS::Serverless::LayerVersion
      Properties:
        LayerName: nodejs-layer-test
        Description: Dependencies for the blank sample app.
        ContentUri: lib/.
        CompatibleRuntimes:
          - nodejs12.x
  ```
- Execute the following `SAM Cli` commands to build and deploy the layer in aws:
  ```aws
  sam build -t template.yaml --use-container

  sam deploy --stack-name lambda-node-test --s3-bucket bucket-name --region us-west-2 --capabilities CAPABILITY_NAMED_IAM
  ```