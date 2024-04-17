import boto3
import csv
from io import StringIO

def lambda_handler(event, context):
    # Define the bucket and key
    bucket_name = 'your-bucket-name'  # Replace with your bucket name
    filename = 'list_ch_lambdas.csv'  # Name of the CSV file in the S3 bucket

    # Define the CMK ARN to use for encryption
    cmk_arn_alias = 'arn:aws:kms:us-region:account:alias/your-cmk-alias'  # Replace with your CMK alias

    # Create an S3 client
    s3 = boto3.client('s3')

    # Get the CSV file from the S3 bucket
    response = s3.get_object(Bucket=bucket_name, Key=filename)
    csv_data = response['Body'].read().decode('utf-8')

    # Parse the CSV data
    csv_file = StringIO(csv_data)
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row

    # Create a Lambda client
    lambda_client = boto3.client('lambda')

    # Update the encryption settings of Environment Variables for each Lambda function
    for row in csv_reader:
        function_name = row[0]
        environment_variables = row[1]

        # Update the encryption settings of the Environment Variables
        response = lambda_client.update_function_configuration(
            FunctionName=function_name,
            Environment={
                'Variables': environment_variables
            },
            KMSKeyArn=cmk_arn_alias
        )
        print(f"Updated the encryption settings for Lambda function: {function_name}")

    return {
        'statusCode': 200,
        'body': 'Lambda encryption settings updated successfully'
    }