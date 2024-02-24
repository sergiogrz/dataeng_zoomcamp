#!/usr/bin/env python

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, TimestampType, StringType, IntegerType, DoubleType
from pyspark.sql.utils import AnalysisException

yellow_schema = StructType([
    StructField('VendorID', IntegerType(), True),
    StructField('tpep_pickup_datetime', TimestampType(), True),
    StructField('tpep_dropoff_datetime', TimestampType(), True),
    StructField('passenger_count', IntegerType(), True),
    StructField('trip_distance', DoubleType(), True),
    StructField('RatecodeID', IntegerType(), True),
    StructField('store_and_fwd_flag', StringType(), True),
    StructField('PULocationID', IntegerType(), True),
    StructField('DOLocationID', IntegerType(), True),
    StructField('payment_type', IntegerType(), True),
    StructField('fare_amount', DoubleType(), True),
    StructField('extra', DoubleType(), True),
    StructField('mta_tax', DoubleType(), True),
    StructField('tip_amount', DoubleType(), True),
    StructField('tolls_amount', DoubleType(), True),
    StructField('improvement_surcharge', DoubleType(), True),
    StructField('total_amount', DoubleType(), True),
    StructField('congestion_surcharge', DoubleType(), True)
])

green_schema = StructType([
    StructField('VendorID', IntegerType(), True), 
    StructField('lpep_pickup_datetime', TimestampType(), True), 
    StructField('lpep_dropoff_datetime', TimestampType(), True), 
    StructField('store_and_fwd_flag', StringType(), True), 
    StructField('RatecodeID', IntegerType(), True), 
    StructField('PULocationID', IntegerType(), True), 
    StructField('DOLocationID', IntegerType(), True), 
    StructField('passenger_count', IntegerType(), True), 
    StructField('trip_distance', DoubleType(), True), 
    StructField('fare_amount', DoubleType(), True), 
    StructField('extra', DoubleType(), True), 
    StructField('mta_tax', DoubleType(), True), 
    StructField('tip_amount', DoubleType(), True), 
    StructField('tolls_amount', DoubleType(), True), 
    StructField('ehail_fee', DoubleType(), True), 
    StructField('improvement_surcharge', DoubleType(), True), 
    StructField('total_amount', DoubleType(), True), 
    StructField('payment_type', IntegerType(), True), 
    StructField('trip_type', IntegerType(), True), 
    StructField('congestion_surcharge', DoubleType(), True)
])

schemas = {
    "yellow": yellow_schema,
    "green": green_schema
}


def main():
    spark = (
        SparkSession.builder.master("local[*]").appName("parquetize datasets").getOrCreate()
    )

    taxi_types = ["yellow", "green"]
    years = [2020, 2021]
    months = range(1, 13)

    for taxi_type in taxi_types:
        for year in years:
            for month in months:
                print(f"Processing {taxi_type} taxi data for {year}/{month:02d}")
                input_path = f"../../data/nyc_tlc/raw/{taxi_type}/{year}/{month:02d}"
                output_path = f"../../data/nyc_tlc/pq/{taxi_type}/{year}/{month:02d}"

                try:
                    df = (
                        spark.read
                        .option("header", True)
                        .schema(schemas[taxi_type])
                        .csv(input_path)
                    )
                except AnalysisException:
                    print(f"Path {input_path} does not exist.")
                    break

                try:
                    df.repartition(4).write.parquet(output_path)
                except AnalysisException:
                    print(f"Path {output_path} already exists.")
                    continue


if __name__ == "__main__":
    main()
