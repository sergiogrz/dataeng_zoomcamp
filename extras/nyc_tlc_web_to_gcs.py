import io
import os
import requests
import pandas as pd
from google.cloud import storage
import argparse
import logging

"""
Pre-reqs: 
1. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
2. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

# logging
logger = logging.getLogger()  # create a logger object instance
logger.setLevel(logging.INFO)  # set the lowest severity for logging
console_handler = logging.StreamHandler() # set a handler or destination for your logs
log_formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d | %H:%M:%S",
)  # set the logging format for your handler
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)  # add the handler to the logger

# switch out the bucketname
BUCKET = os.environ.get("GCP_GCS_BUCKET", "dtc-data-lake-bucketname")


def upload_to_gcs(bucket, object_name, content):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_string(content)


def web_to_gcs(params):
    service = params.service
    year = params.year
    months = params.months
    # https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2019-01.parquet
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"

    for month in months:
        logger.info(f"Service: {service}, year: {year}, month: {month}")
        file_name = f"{service}_tripdata_{year}-{month:02}.parquet"
        logger.info(f"File name: {file_name}")
        url = f"{base_url}/{file_name}"
        logger.info(f"URL: {url}")

        response = requests.get(url)
        if response.status_code == 200:
            logger.info("Uploading Parquet file to GCS")
            upload_to_gcs(BUCKET, f"{service}/{file_name}", response.content)
            logger.info(f"Uploaded Parquet to GCS: {service}/{file_name}")

        else:
            logger.warning(f"Failed to download Parquet from: {url}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download CSV files from the web and upload them to GCS as parquet files")

    parser.add_argument("--service", help="Service name ('yellow', 'green', 'fhv').")
    parser.add_argument("--year", help="Year from which you want to download data.")
    parser.add_argument("--months", nargs='+', type=int, default=list(range(1, 13)),
                        help="List of integers representing months. Default is 1 to 12 inclusive.")

    args = parser.parse_args()

    web_to_gcs(args)
