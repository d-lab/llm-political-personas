import pandas as pd
from io import BytesIO
import boto3
import os
import json
from botocore.exceptions import ClientError
from colorama import Fore, init
# Initialize colorama for colored output
init(autoreset=True)

# Initialize S3 client
s3_client = boto3.client('s3')

# Set default bucket and key
DEFAULT_BUCKET = os.environ.get('DEFAULT_S3_BUCKET', 'sagemaker-us-east-1-010438503570')
DEFAULT_KEY = 'Persona/data/'


# --------------------------- READ FROM S3 ----------------------------------
def read_s3_csv(key, bucket=None, **kwargs):
    """Given a bucket and a key (path to a .csv file) returns a dataframe"""
    bucket = bucket or DEFAULT_BUCKET
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(BytesIO(obj['Body'].read()), **kwargs)
        if isinstance(df, pd.DataFrame):
            return df
        else:
            raise ValueError(f"Failed to read CSV. Returned object is not a DataFrame: {type(df)}")
    except Exception as e:
        print(f"Error reading CSV from S3: {str(e)}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

def read_s3_parquet(key, bucket=None):
    """Given a bucket and a key (path to a .pqt file) returns a dataframe"""
    bucket = bucket or DEFAULT_BUCKET
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    return pd.read_parquet(BytesIO(obj['Body'].read()))

def read_s3_text(key, bucket=None):
    """Given a bucket and a key (path to a .txt file) returns it"""
    bucket = bucket or DEFAULT_BUCKET
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    return obj['Body'].read().decode('utf-8')

def read_s3_json(key, bucket=None):
    """
    Given a bucket and a key (path to a .json file) returns the parsed JSON data
    
    Args:
        key (str): The S3 key (path) to the JSON file
        bucket (str, optional): The S3 bucket name. Defaults to DEFAULT_BUCKET
    
    Returns:
        dict/list: Parsed JSON data
    """
    bucket = bucket or DEFAULT_BUCKET
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        json_data = json.loads(obj['Body'].read().decode('utf-8'))
        return json_data
    except Exception as e:
        print(f"Error reading JSON from S3: {str(e)}")
        return {} if '{}' in str(e) else []
# --------------------------- READ FROM S3 ----------------------------------


# --------------------------- WRITE TO S3 -----------------------------------
def write_s3_csv(df, key, bucket=None):
    """Given a dataframe, a bucket and a key save the dataframe in .csv"""
    bucket = bucket or DEFAULT_BUCKET
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    s3_client.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())

def write_s3_parquet(df, key, bucket=None):
    """Given a dataframe, a bucket and a key save the dataframe in .pqt"""
    bucket = bucket or DEFAULT_BUCKET
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, index=False, compression='gzip')
    s3_client.put_object(Bucket=bucket, Key=key, Body=parquet_buffer.getvalue())

def write_s3_json(data, key, bucket=None, indent=4):
    """
    Write JSON data to an S3 bucket
    
    Args:
        data (dict/list): The data to be written as JSON
        key (str): The S3 key (path) where the JSON file will be saved
        bucket (str, optional): The S3 bucket name. Defaults to DEFAULT_BUCKET
        indent (int, optional): Number of spaces for JSON formatting. Defaults to 2
    """
    bucket = bucket or DEFAULT_BUCKET
    try:
        json_str = json.dumps(data, indent=indent)
        s3_client.put_object(Bucket=bucket, Key=key, Body=json_str)
    except Exception as e:
        print(f"Error writing JSON to S3: {str(e)}")
# --------------------------- WRITE TO S3 -----------------------------------


# --------------------------- UPLOAD TO S3 ----------------------------------
def upload_file_to_s3(local_path, bucket, s3_path):
    s3_client.upload_file(local_path, bucket, s3_path)

def upload_directory_to_s3(local_dir, bucket, s3_prefix):
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_dir)
            s3_path = os.path.join(s3_prefix, relative_path).replace("\\", "/")
            s3_client.upload_file(local_path, bucket, s3_path)
# --------------------------- UPLOAD TO S3 ----------------------------------


# ----------------------- LIST BUCKETS AND FILES IN S3 ----------------------
def list_s3_buckets():
    """Lists all the buckets available"""
    try:
        response = s3_client.list_buckets()
        print("Available S3 buckets:")
        for bucket in response['Buckets']:
            print(f"  - {bucket['Name']}")
    except ClientError as e:
        print(f"Error listing buckets: {e}")

def print_s3_contents(prefix=DEFAULT_KEY, bucket=None):
    """Prints the content of S3 sub-directories"""
    bucket = bucket or DEFAULT_BUCKET
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for item in page.get('Contents', []):
                key = item['Key']
                if key.endswith('/'):
                    print(f"  {key}")
                elif '.' in key.split('/')[-1]:  # Check if the filename contains a dot
                    print(f"  {Fore.RED}{key}{Fore.RESET}")
                else:
                    print(f"  {key}")
    except ClientError as e:
        print(f"Error listing contents of bucket '{bucket}': {e}")
        # ----------------------- LIST BUCKETS AND FILES IN S3 ----------------------
