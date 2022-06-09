## Sample Jenkinsfile for aws deployment

### Steps
1. Create an IAM role with trust policy for the Role of the Jenkins instance from where the deployment will happen. 
    - Sample trust policy [here](../aws/iam/jenkins_trust_policy.json).
    - Sample jenkins permissions [here](../aws/iam/jenkins_sample_permissions.json)
2. In the jenkinsfile, assume the role created above to perform the deployment actions.

### Sample Jenkinsfile
The following jenkinsfile uses a deployment script ([sample](../aws/cloudformation/1.sample_shell_script_for_deployment.sh) ) written in shell and a cloudformation template ([sample](../aws/cloudformation/lambda-node-with-role-non-serverless.yaml)) to deploy code into prod, stage or dev aws account depending on the branch where the code is committed. The shell script contains various variables specific to the environment where the services are being deployed. 

- The `environment` section of the code is used to determine which role the process should assume for deployment
- The `Move Env Files` stage is used to rename the relevant env file to .env so that the correct variables are passed by the deployment script to the cloudformation template
- The `Zip Function` stage is used to zip relevant files needed by the cloudformation template. Note that while the scripts for most of the other stages are shell-scripts, this one is not.
- In the final stage -  `Deploy Services`, the account specific IAM role is assumed, the aws secrets are obtained and the relevant deployment script is executed.

```groovy
def jnlpDockerImage = 'docker.artifactory.a.xxx.com/dev/build/ibp/jnlp-slave-with-docker:3.26-1_jenkins-2-138-update_3'

def jenkinsRole = 'arn:aws:iam::123456789:role/<jenkins-role-name>'

pipeline {
    agent {
        kubernetes {
            label "s3-access-test-${UUID.randomUUID().toString()}"
            yaml """
                  apiVersion: v1
                  kind: Pod
                  metadata:
                    annotations:
                      iam.amazonaws.com/role: ${jenkinsRole}
                  spec:
                    containers:
                    - name: jnlp
                      image: ${jnlpDockerImage}
                      volumeMounts:
                      - name: docker-volume
                        mountPath: /var/run/docker.sock
                    volumes:
                    - name: docker-volume
                      hostPath:
                        path: /var/run/dind/docker.sock
                  """
        }
    }
    environment {
        DEV_ROLE = 'arn:aws:iam::123456789:role/<jenkins-role-name-in-the-account>'
        STG_ROLE = 'arn:aws:iam::123456897:role/<jenkins-role-name-in-the-account>'
        PRD_ROLE = 'arn:aws:iam::123456978:role/<jenkins-role-name-in-the-account>'
    }

    stages {
        stage('Set Env') {
            steps {
                script {
                    sh '''
                        echo "env.WORKSPACE: ${WORKSPACE}"

                        cd ${WORKSPACE}

                        echo ${GIT_COMMIT} > gitcommit.txt
                        echo ${GIT_BRANCH} >> gitcommit.txt
                        echo ${GIT_URL} >> gitcommit.txt
                        echo ${GIT_AUTHOR_NAME} >> gitcommit.txt
                    '''
                }
            }
        }
       stage('Move Env Files'){
          steps{
             script{
                    sh '''
                        cd folder-name
                        if [ "${GIT_BRANCH}" = "develop" ]; then
                            cp dev.env src/.env
                        elif [ "${GIT_BRANCH}" = "release" ]; then
                            cp stage.env src/.env
                        elif [ "${GIT_BRANCH}" = "master" ]; then
                            cp prod.env src/.env
                        fi
                    '''
             }
          }
       }
       stage('Zip Function'){
          steps{
             script{
                    zip zipFile: 'file.zip', archive: false, overwrite: true, dir: './path/to/zip/'
             }
          }
       }
        stage('Deploy Services') {
            steps {
                script {
                    sh '''
                        if [ "${GIT_BRANCH}" = "develop" ]; then
                            temp_role=$(aws sts assume-role --role-arn ${DEV_ROLE} --role-session-name AWSCLI-Session)
                        elif [ "${GIT_BRANCH}" = "release" ]; then
                            temp_role=$(aws sts assume-role --role-arn ${STG_ROLE} --role-session-name AWSCLI-Session)
                        elif [ "${GIT_BRANCH}" = "master" ]; then
                            temp_role=$(aws sts assume-role --role-arn ${PRD_ROLE} --role-session-name AWSCLI-Session)
                        fi
                        
                        echo ${temp_role}

                        export AWS_ACCESS_KEY_ID=$(echo ${temp_role} | jq .Credentials.AccessKeyId | xargs)
                        export AWS_SECRET_ACCESS_KEY=$(echo ${temp_role} | jq .Credentials.SecretAccessKey | xargs)
                        export AWS_SESSION_TOKEN=$(echo ${temp_role} | jq .Credentials.SessionToken | xargs)

                        mv file.zip dir/new_file.zip

                        cd dir
                        ls
                        if [ "${GIT_BRANCH}" = "develop" ]; then
                            echo "Deploying to Dev"
                            ./deploydev.sh
                        elif [ "${GIT_BRANCH}" = "release" ]; then
                            echo "Deploying to Stage"
                            ./deploystg.sh
                        elif [ "${GIT_BRANCH}" = "master" ]; then
                            echo "Deploying to Prod"
                            ./deployprd.sh
                        fi
                    '''
                }
            }
        }
    }
}

```