import argparse
import logging
import os
import requests
import yaml
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud import storage


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

# configuration files for schema and column names
schema = "./schema.yml"
rename_cols = "./rename_cols.yml"


def upload_to_gcs(bucket, object_name, file_name):
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
    blob.upload_from_filename(file_name)


def web_to_gcs(params):
    service = params.service
    year = params.year
    months = params.months
    # https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2019-01.parquet
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"

    # schema
    with open(schema, "rb") as f:
        service_schema = yaml.safe_load(f)[service]

    # column names mapping
    with open(rename_cols, "rb") as f:
        service_rename_cols = yaml.safe_load(f)[service]

    for month in months:
        logger.info(f"Service: {service}, year: {year}, month: {month}")
        file_name = f"{service}_tripdata_{year}-{month:02}.parquet"
        logger.info(f"File name: {file_name}")
        url = f"{base_url}/{file_name}"
        logger.info(f"URL: {url}")

        response = requests.get(url)
        if response.status_code == 200:
            logger.info("Reading and formatting Parquet file to a DataFrame")
            df = (pd.read_parquet(url,
                                  engine="pyarrow",
                                  columns=list(service_schema.keys()))
                                  .astype(service_schema))
            df = df.rename(columns=service_rename_cols)
            logger.info("Saving formatted Parquet file locally")
            # df.to_parquet(file_name, engine='pyarrow')
            table = pa.Table.from_pandas(df)
            pq.write_table(table, file_name)

            # logger.info("Loading Parquet file to GCS")
            # upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
            # logger.info(f"Uploaded Parquet to GCS: {service}/{file_name}")
            # os.remove(file_name)
            # logger.info(f"{file_name} removed locally")

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
