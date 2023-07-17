# Welcome to your CDK TypeScript project

You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`CdkWorkshopStack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template

## Project Structure

- `lib/cdk-workshop-stack.ts` is where your **CDK application’s main stack** is defined. This is the file we’ll be spending most of our time in.
- `bin/cdk-workshop.ts` is the **entrypoint of the CDK application**. It will load the stack defined in lib/cdk-workshop-stack.ts.
- `package.json` is your npm module manifest. It includes information like the name of your app, version, dependencies and build scripts like “watch” and “build” (package-lock.json is maintained by npm)
- `cdk.json` tells the toolkit **how to run your app**. In our case it will be "npx ts-node bin/cdk-workshop.ts"
- `tsconfig.json` your project’s **typescript configuration**
- `.gitignore` and `.npmignore` tell git and npm which files to include/exclude from source control and when publishing this module to the package manager.
node_modules is maintained by npm and includes all your project’s dependencies.

## Project Synthesis
When CDK apps are executed, they produce an AWS CloudFormation template for each stack defined in the application. The template json file is generated in the cdk.out folder
Use the `cdk synth` command to synthesize a CDK app. 
The CDK CLI requires you to be in the same directory as your cdk.json file.

## Bootstrap
The **FIRST TIME** you deploy an AWS CDK app into an environment (account/region), you can install a “bootstrap stack”. This stack includes resources that are used in the toolkit’s operation:
- `SSM Parameter` for the CDK Bootstrap version
- `IAM Roles and Policies` (if needed) for CloudFormation execution, Deployment action, File and Image publishing and Lookup
- `ECR Repository` for container assets
- `S3 bucket` and policy for staging templates and assets

Use `cdk bootstrap` command to install the bootstrap stack into an environment

## Checking Differences
Use `cdk diff` to show the difference between the modifications to the CDK app and what’s currently deployed

## Deploy
Use `cdk deploy` to deploy a CDK app