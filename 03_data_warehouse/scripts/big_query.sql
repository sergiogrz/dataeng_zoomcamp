-- Query public available table
SELECT station_id, name FROM
    bigquery-public-data.new_york_citibike.citibike_stations
LIMIT 100;


-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE <project_id>.ny_taxi.external_yellow_taxi_data
OPTIONS (
  format = 'Parquet',
  uris = ['gs://<bucket_name>/yellow/yellow_tripdata_2019*.parquet',
          'gs://<bucket_name>/yellow/yellow_tripdata_2020*.parquet']
);

-- Check yellow trip data
SELECT * FROM <project_id>.ny_taxi.external_yellow_taxi_data limit 10;

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE <project_id>.ny_taxi.yellow_taxi_data_non_partitioned AS
SELECT * FROM <project_id>.ny_taxi.external_yellow_taxi_data;


-- Create a partitioned table from external table
CREATE OR REPLACE TABLE <project_id>.ny_taxi.yellow_taxi_data_partitioned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM <project_id>.ny_taxi.external_yellow_taxi_data;

-- Impact of partition
-- Non-partitioned
SELECT DISTINCT(VendorID), passenger_count, tip_amount, total_amount, trip_distance
FROM <project_id>.ny_taxi.yellow_taxi_data_non_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-01-01' AND '2019-01-31';

-- Partitioned
SELECT DISTINCT(VendorID), passenger_count, tip_amount, total_amount, trip_distance
FROM <project_id>.ny_taxi.yellow_taxi_data_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-01-01' AND '2019-01-31';

-- Let's look into the partitons
SELECT table_name, partition_id, total_rows
FROM `ny_taxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_taxi_data_partitioned'
ORDER BY total_rows DESC;

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE <project_id>.ny_taxi.yellow_taxi_data_partitioned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM <project_id>.ny_taxi.external_yellow_taxi_data;

-- Impact of clustering
-- Partitioned
SELECT count(*) as trips
FROM <project_id>.ny_taxi.yellow_taxi_data_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-01-01' AND '2019-02-15'
  AND VendorID=1;

--Partitioned and clustered
SELECT count(*) as trips
FROM <project_id>.ny_taxi.yellow_taxi_data_partitioned_clustered
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-01-01' AND '2019-02-15'
  AND VendorID=1;