import os, requests
import zipfile
from io import BytesIO
import boto3
from botocore.client import Config

USER = os.getenv('API_USER')
PASSWORD = os.environ.get('API_PASSWORD')
DOWNLOAD_URL = os.environ.get("DOWNLOAD_URL")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
AWS_REGION_NAME = os.environ.get("AWS_REGION")
AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")

def download_file(url):
    print(f"Starting data transfer from {url}")
    get_response = requests.get(url, stream=True, auth=(USER, PASSWORD))
    return get_response.content


def unzip_and_upload_to_s3(content):
    data = BytesIO(content)
    s3 = boto3.client('s3',
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_KEY,
                        config=Config(signature_version='s3v4'),
                        region_name=AWS_REGION_NAME)

    with zipfile.ZipFile(data) as zip:
        for name in zip.namelist():
            print(f"Unpacking and moving to S3 {name}...")
            s3.upload_fileobj(zip.open(name, 'r'), AWS_BUCKET_NAME, name)


content = download_file(DOWNLOAD_URL)
unzip_and_upload_to_s3(content)
