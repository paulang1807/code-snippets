# Content
- [Create Lambda Layer for Python packages](#create-lambda-layer-for-python-packages)
- [Create Lambda Function and Layer for Node Js Code](#create-lambda-function-and-layer-for-node-js-code)
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
  ```bash
  docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.8" /bin/sh -c "pip install -r requirements.txt -t python/lib/python3.8/site-packages/; exit"
  ```
  - This will create a folder and add the output of the `pip install` command in the folder.
- Zip the folder created above
  ```bash
  zip -r <zip_file_name>.zip python > /dev/null
  ```
-Upload the zip file to s3
- Create a `CloudFormation` template (layer.yml) for creating the layer in aws. Sample template [here](../cloudformation/serverless-lambda-layer-python.yaml).
- Execute the following `SAM Cli` commands to build and deploy the layer in aws:
  ```aws
  sam build -t layer.yaml --use-container

  sam deploy --stack-name lambda-layer-test --s3-bucket bucket-name --region us-west-2 --capabilities CAPABILITY_NAMED_IAM
  ```

## Create Lambda Function and Layer for Node Js Code

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
- Create a `CloudFormation` template (layer.yml) for creating the layer in aws. Sample template [here](../cloudformation/serverless-lambda-function-with-layer-nodejs.yaml)
- Execute the following `SAM Cli` commands to build and deploy the layer in aws:
  ```aws
  sam build -t template.yaml --use-container

  sam deploy --stack-name lambda-node-test --s3-bucket bucket-name --region us-west-2 --capabilities CAPABILITY_NAMED_IAM
  ```