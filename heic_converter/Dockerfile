FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    imagemagick \
    libheif-dev \
    python3 \
    python3-pip \
    awscli

# Install boto3 for S3 access
RUN pip3 install boto3

# Copy your conversion script
COPY convert.py /app/convert.py
WORKDIR /app

# Lambda entry point
CMD ["python3", "convert.py"]
