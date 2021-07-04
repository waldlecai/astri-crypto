## Identity Service REST APIs for ASTRI Crypto Trading Platform

This is a readme guide for deploying Identity Service REST APIs for ASTRI Crypto Trading Platform based on following technology stack
- Serverless Framework - Zapper 
- Web Application Framework - Flask 
- AWS Lambda 
- AWS API Gateway 
- AWS Cognito User Pool 

### Technology Stack Overview 
Zappa is a Python package that bundles up web apps written in Flask or Django and deploys them to AWS (Amazon Web Services) Lambda. Lambda is Amazon's function as a service (FaaS) platorm. Instead of deploying your Flask or Django web app on a cloud server, like an AWS EC2 instance, you can deploy your app serverless as an AWS Lambda function.  
  
Flask is a Python micro framework for building WSGI web application. Flask supports all kinds of extensions that can add application features as and when needed. It's chosen as the basic framework for implementing all REST APIs in the entire ASTRI Crypto Trading project.  

With AWS Lambda, you don't have to spin up servers, install packages, make sure security patches are up to date, most of all, you don't have to pay for server time that isn't used.  
So as long as your web traffic is low, running a web application serverless on AWS Lambda is pretty cheap compared to running a regular cloud server. Serverless Lambda functions scale up and down based on demand.  
  
AWS API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. In the ASTRI Crypto Trading platform project, APIs act as the "front door" for applications to business logic (i.e. users management, trade orders management etc), access data (i.e. quotes and quotes data). Using API Gateway, you can create REST APIs and WebSocket APIs that enable real-time two-way communication applications.  
  
AWS Cognito User Pool is a user directory in AWS Cognito, a fully managed identity service offered by AWS. With a user pool, you can allow people to signup with their email address and a password. Cognito confirms the registration by sending the user a code to the email address. AWS Cognito user pool also provides rich APIs for user management, which dramatically resduces development effort to buid a scalable identify service.  
  
### Installing Zappa and Flask
Before you can deploy the Flask based REST APIs web app on AWS Lambda with Zappa, you first need to install Zappa and the web framework Flask to build our web app with.  
  
Clone this git repository into a project directory and "cd" into it. Create a Python virtual environment, activate it, and install Zappa and Flask.  
  
```
git clone https://github.com/waldlecai/astri-crypto.git
cd astri-crypto
python -m venv venv
source venv/bin/activate
pip install flask
pip install zappa
```
  
### Configuring AWS Credentials  
Before you can use Zappa to automate deployment this Identity Service REST APIs onto AWS, you need to properly create AWS Access Keys for satisfying AWS Identity & Access Management requirement.  
- Create AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY for programmatic access by following [AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys) (Programmatic access section)  
- Obtain existing or create new COGNITO_USER_CLIENT_ID, COGNITO_USER_POOL_ID for accessing AWS Cognito User Pool by following [Configuring AWS Cognito User Pool App Client](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html)  
- Update .env file under this project directory with above obtained credentials where "XXXXXX" refers to the placeholders for credentials  
```
AWS_ACCESS_KEY_ID=XXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXX
REGION_NAME=us-east-1
COGNITO_USER_CLIENT_ID=XXXXXXXXXXXXXX
COGNITO_USER_POOL_ID=XXXXXXXXXXXX
```  
All above parameters defined in .env file are treated as environment variables retrieved programmatically using an open source Python libary called "dotenv". Following code snippet in cognito_handler.py. demonstrates how it's used to retrieve environment variables in code.  
```
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
dotenv_path = os.path.join(os.path.dirname(os.path.abspath("__file__")), ".env")
load_dotenv(dotenv_path)
self.client = boto3.client("cognito-idp", region_name=os.getenv("REGION_NAME"))
self.client_id = os.getenv("COGNITO_USER_CLIENT_ID")
self.user_pool_id=os.getenv("COGNITO_USER_POOL_ID")
```
### Using Zappa  
#### Initial Deployment
Before we can deploy Serverless Flask REST APIs, we need to initialize Zappa's configuration by running:
```
zappa init
```
This command will generate zappa_setting.json specific for project contained within current project folder, similar to following:  
```
{
    "dev": {
        "app_function": "id_service.app", ## this reflects the main python file and entry point of Flask web app
        "aws_region": "us-east-1",        ## the AWS region to be deployed to
        "profile_name": "default",        ## corresponds to the name in square brackets in .aws/credentials
        "project_name": "astri-crypto",   ## Zappa project name derived from project folder name
        "runtime": "python3.8",           ## Python runtime
        "s3_bucket": "zappa-231dlgkmh".   ## Zappa automatically creates a random S3 bucket for uploading and deploying Serverless App package
    }
}
```  
Initial deployment of Serverless Flask app on AWS Lambda can be done by running following command where either of 'dev'|'staging'|'production' can be used corresponding the environment in question:  
```
zappa deploy dev
```  
#### Updates Deployment  
If application code has bene updated, changes can be packaged and deployed onto AWS using following command where either of 'dev'|'staging'|'production' can be used corresponding the environment in question:  
```
zappa update dev
```  
#### Undeploy  
The entire Serverless Flask app stack incuding API Gateway, Lambda functions can be undeployed by running following command where either of 'dev'|'staging'|'production' can be used corresponding the environment in question.  
```
zappa undeploy dev
```
