-- Create an external table using the Green Taxi Trip Records Data for 2022
CREATE OR REPLACE EXTERNAL TABLE <project_id>.ny_taxi.external_green_taxi_data
OPTIONS (
format = 'Parquet',
uris = ['gs://<bucket_name>/green/green_tripdata_2022*.parquet']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE <project_id>.ny_taxi.green_taxi_data AS
SELECT * FROM <project_id>.ny_taxi.external_green_taxi_data;


-- What is count of records for the 2022 Green Taxi Data?
SELECT COUNT(1) FROM <project_id>.ny_taxi.green_taxi_data;


-- Count the distinct number of PULocationIDs for the entire dataset on both the tables
-- External table
SELECT COUNT(DISTINCT PULocationID) FROM <project_id>.ny_taxi.external_green_taxi_data;

-- Materialized table
SELECT COUNT(DISTINCT PULocationID) FROM <project_id>.ny_taxi.green_taxi_data;


-- How many records have a fare_amount of 0?
SELECT COUNT(1) FROM <project_id>.ny_taxi.green_taxi_data
WHERE fare_amount = 0;


-- Create a table partitioned by lpep_pickup_datetime and clustered by PUlocationID
CREATE OR REPLACE TABLE <project_id>.ny_taxi.green_taxi_data_partitioned_clustered
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID AS
SELECT * FROM <project_id>.ny_taxi.green_taxi_data;


-- Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime
-- 06/01/2022 and 06/30/2022 (inclusive)
-- Non partitioned or clustered table
SELECT DISTINCT (PULocationID) FROM <project_id>.ny_taxi.green_taxi_data
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

-- Partitioned and clustered table
SELECT DISTINCT (PULocationID) FROM <project_id>.ny_taxi.green_taxi_data_partitioned_clustered
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';


-- Count the number of records
SELECT COUNT(*) FROM <project_id>.ny_taxi.green_taxi_data;

