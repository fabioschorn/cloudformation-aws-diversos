import boto3
import csv
from io import StringIO

def lambda_handler(event, context):
    # Define the bucket and key
    bucket_name = 'your-bucket-name'  # Replace with your bucket name
    key = 'list_ch_lambdas.csv'  # Name of the CSV file in the S3 bucket
    
    # Create an S3 client
    s3_client = boto3.client('s3')
    # Create a Lambda client
    lambda_client = boto3.client('lambda')
    
    # Retrieve the CSV file from S3
    csv_obj = s3_client.get_object(Bucket=bucket_name, Key=key)
    csv_body = csv_obj['Body'].read().decode('utf-8')
    
    # Convert the CSV data into a list of ARNs
    arns = []
    csv_reader = csv.reader(StringIO(csv_body))
    for row in csv_reader:
        arns.append(row[0])  # Assuming the ARN is in the first column of each row
    
    # Specify the alias of your CMK
    kms_key_alias = 'alias/personal_key'  # Replace 'personal_key' with your CMK alias
    
    # Update each Lambda function's configuration to use the specified KMS key alias
    for arn in arns:
        response = lambda_client.update_function_configuration(
            FunctionName=arn,
            KMSKeyArn=kms_key_alias
        )
        print(f"Updated {arn} to use KMS key alias {kms_key_alias}")

# Be sure to replace 'your-bucket-name' and 'list_ch_lambdas.csv' with the actual S3 bucket and file path.
# Also, replace 'alias/personal_key' with the actual alias of your KMS key.