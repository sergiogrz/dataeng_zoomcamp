#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import logging
from time import time
import pandas as pd
from sqlalchemy import create_engine  # connect to Postgres database

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


def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table = params.table
    url = params.url

    # Download the csv file
    # the backup files are gzipped, and it's important for pandas to keep the
    # correct extension to be able to open the file
    if url.endswith(".csv.gz"):
        csv_name = "output.csv.gz"
    else:
        csv_name = "output.csv"

    os.system(f"wget {url} -O {csv_name}")

    # Create a connection to Postgres
    # postgresql://username:password@host:port/dbname
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    engine.connect()

    # Generate the database schema and load the first chunk
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    t_start = time()
    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table, con=engine, if_exists="replace")

    # Insert the data into the database
    df.to_sql(name=table, con=engine, if_exists="append")
    t_end = time()
    logger.info(f"Inserted first chunk, took {(t_end - t_start):3f} seconds.")

    while True:
        try:
            t_start = time()
            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(name=table, con=engine, if_exists="append")
            t_end = time()
            logger.info(f"Inserted another chunk, took {(t_end - t_start):3f} seconds.")

        except StopIteration:
            logger.info("Finished ingesting data into the postgres database")
            break


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    # postgresql://username:password@host:port/dbname
    parser.add_argument("--user", help="user name for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database name")
    parser.add_argument(
        "--table", help="table name where the data will be populated into"
    )
    parser.add_argument("--url", help="url of the csv file")

    args = parser.parse_args()

    main(args)
