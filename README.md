#### Note
Sample project to explore on how to build end to end machine learning pipeline along with deployment on AWS EC2.

## Tech stack: Python, Postgres DB, PL/SQL, Git, DVC, Docker, AWS ECR, EC2, CI/CD using Github Actions.

# USA Visa Predictor

The Immigration and Nationality Act (INA) of the US permits foreign workers to come to the United States to work on either a temporary or permanent basis. The act also protects US workers against adverse impacts on working place and maintain requirements when they hire foreign workers to fill workforce shortages. The immigration programs are administered by the Office of Foreign Labor Certification (OFLC).

## Problem

1. OFLC gives job certification applications for employers seeking to bring foreign workers into the United States and grants certifications.
2. As In last year the count of employees were huge so OFLC needs Machine learning models to shortlist visa applicants based on their previous data.

#### In this project we are going to build classification model using the given dataset.
* The model is use to if visa get approved or not based on the given dataset.
* This can be used to recommend suitable profile of the applicants for whom the visa should be granted or denied based on the criteria.


## Dataset

Dataset can be accessed from kaggle https://www.kaggle.com/datasets/moro23/easyvisa-dataset

The data consists of 25480 Rows and 12 Columns

| Feature       | Description                     | 
|---------------|---------------------------------|
| case_id| ID of each visa application     | 
| continent | Information of continent of the employee| 
| education_of_employee     | Information of education of the employee  |
| has_job_experience| Does the employee has any job experience? Y= Yes; N = No     | 
| requires_job_training | Does the employee require any job training? Y = Yes; N = No| 
| no_of_employees     | Number of employees in the employer's company  |
| yr_of_estab | Year in which the employer's company was established| 
| region_of_employment     | Information of foreign worker's intended region of employment in the US.  |
| prevailing_wage| Average wage paid to similarly employed workers in a specific occupation in the area of intended employment. <br/> The purpose of the prevailing wage is to ensure that the foreign worker is not underpaid compared to other workers offering the same or similar service in the same area of employment.     | 
| unit_of_wage | Unit of prevailing wage. Values include Hourly, Weekly, Monthly, and Yearly.| 
| full_time_position     | Is the position of work full-time? Y = Full Time Position; N = Part Time Position |
| case_status     | Flag indicating if the Visa was certified or denied  |



## Project Structure

```
├── LICENSE            
├── Makefile            
├── README.md          
├── data
│   ├── external       
│   ├── interim        
│   ├── processed      
│   └── raw            
│
├── docs               
│
├── models             
│
├── notebooks          
│                            
├── references         
│
├── reports            
│   └── figures        
│
├── mlflow            
│   └── Dockerfile 
├── .github            
│   └── workflows 
│       └── ci-cd.yml
├── .env
├── .gitignore
├── .dvcignore  
├── Dockerfile
├── compose.yaml  
├── dvc.lock 
├── dvc.yaml 
├── pyproject.toml 
├── requirements.txt                 
├── setup.cfg   
├── setup.py                        
├── setup.cfg 
│
└── src                
    │
    ├── __init__.py    
    │
    ├── config         
    │   ├── __init__.py
    │   └── config.py
    │ 
    ├── constants         
    │   └── __init__.py 
    │   
    ├── data_access         
    │   ├── __init__.py
    │   └── usvisa_data.py
    │
    ├── db         
    │   ├── __init__.py
    │   └── db_connector.py
    │
    ├── exception         
    │   └── __init__.py 
    │   
    ├── load_data         
    │   ├── create_schema.py
    │   └── db_schema.sql
    │
    ├── logger   
    │   └── __init__.py      
    │   
    │  
    ├── pipeline         
    │   ├── __init__.py
    │   |── prediction_pipeline.py
    │   └── training_pipeline.py
    │
    ├── utils         
    │   └── __init__.py 
    │
    │
    └── components         
       ├── __init__.py
       |── data_ingestion.py
       |── data_transformation.py
       └── model_trainer.py
```

--------


## Setup and Installation

## Prerequisites
Before you begin the installation process, ensure you have the following:

* An Anaconda distribution of Python 3.8 or higher
* Git for cloning the repository
* Access to a terminal or command-line interface

## Installation Steps

1. Clone the repository to your local machine using Git:

    
    ```git https://github.com/surekhag28/us-visa-predictor-ml-pipeline.git```            
    ```cd us-visa-predictor-ml-pipeline ```

2. Create and Activate a Conda Environment:

    ```conda create -n venv python=3.11 -y```
    ```conda activate venv```

3. Install Dependencies

    ```pip install -r requirements_dev.txt```


## AWS Services Setup
    
Log in to the AWS Console and perform the following:

* Create an IAM User for Deployment
* Assign the following policies for necessary access:
* AmazonEC2ContainerRegistryFullAccess for ECR access.
* AmazonEC2FullAccess for EC2 access.
* AmazonS3FullAccess for S3 access.

#### Create an S3 Bucket

Navigate to the Amazon S3 service and create a bucket:

* Bucket Name: dvc-s3-remote
* Region: Select your preferred AWS region
* Permissions: Ensure the bucket is accessible to your IAM user.

#### Create an ECR Repository

Navigate to the Amazon ECR service and create a new repository. Note the URI:

e.g., <account_id>.dkr.ecr.ap-southeast-2.amazonaws.com/usa_visa_predictor_repo

#### Postgres DB Setup

Create a Postgres Database
* Download and Install postgresql server on machine.
* Run command ```python src/load_data/create_schema.py``` for generating DB schema and inserting data into table.

#### Configure Environment Variables:

Before running the application, set up the necessary environment variables in .env file under project folder.

#### DB credentials

* DB_HOST
* DB_PORT
* DB_NAME
* DB_USER
* DB_PASSWORD

#### AWS credentials
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_REGION

#### Running the application

* Make sure that Docker is installed on machine.

First build the docker image

```docker compose build```

Run the docker container

```docker compose up -d```

The machine learning pipeline stages configured in dvc.yaml file will run sequentially for both training the model and predictions at the end.

## AWS CI/CD Deployment with GitHub Actions

#### Set Up GitHub Secrets

Add the following secrets in your GitHub repository settings under Secrets:

* AWS_ACCESS_KEY_ID: Your IAM user's access key.
* AWS_SECRET_ACCESS_KEY: Your IAM user's secret access key.
* AWS_REGION: Your AWS default region (e.g., us-east-1).
* AWS_ACCOUNT_ID: Your IAM user's account id
* ECR_REPOSITORY: The URI of your ECR repository.

#### Define the CI/CD Workflow

.github/workflows/ci-cd.yml file to automate the deployment

* Create python virtual environment.
* Install all the required Dependencies.
* Build and Test the docker image on virtual environment.
* Authenticate AWS credentials.
* Login to AWS ECR.
* Build, tag and push the image to ECR.
