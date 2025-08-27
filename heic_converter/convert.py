import boto3
import subprocess
import os

s3 = boto3.client('s3')

def convert_image(bucket, key):
    input_path = '/tmp/input.jpg'
    output_path = '/tmp/output.heic'

    # Download from S3
    s3.download_file(bucket, key, input_path)

    # Convert using ImageMagick
    subprocess.run(['magick', input_path, output_path], check=True)

    # Upload to converted-images/
    output_key = 'converted-images/' + os.path.basename(key).replace('.jpg', '.heic')
    s3.upload_file(output_path, bucket, output_key)

# Example invocation
def lambda_handler(event, context):
    bucket = event['bucket']
    key = event['key']
    convert_image(bucket, key)
