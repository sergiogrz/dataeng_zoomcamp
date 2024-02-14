# Module 3 Homework Solutions

> [!NOTE]  
> The SQL queries for this homework can also be found in the [hw_big_query.sql](./hw_big_query.sql) file.

## Setup

### Load files to GCS

For this homework we need the 2022 NYC Green Taxi Parquet Files from 2022 ([link to the website](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)). In order to load these file to our bucket in Google Cloud Storage, we follow the steps from the [README file](../../extras/README.md) and make use of the `nyc_tlc_web_to_gcs.py` script.


### Create tables in BigQuery

* Create an external table using the Green Taxi Trip Records Data for 2022.
    ```sql
    -- Create an external table using the Green Taxi Trip Records Data for 2022
    CREATE OR REPLACE EXTERNAL TABLE <project_id>.ny_taxi.external_green_taxi_data
    OPTIONS (
    format = 'Parquet',
    uris = ['gs://<bucket_name>/green/green_tripdata_2022*.parquet']
    );
    ```

* Create a table in BQ using the Green Taxi Trip Records for 2022 (do not partition or cluster this table).
    ```sql
    -- Create a non partitioned table from external table
    CREATE OR REPLACE TABLE <project_id>.ny_taxi.green_taxi_data AS
    SELECT * FROM <project_id>.ny_taxi.external_green_taxi_data;
    ```



## Questions

### Question 1

**Question:** What is count of records for the 2022 Green Taxi Data?

**Answer:** 840,402.

```sql
-- What is count of records for the 2022 Green Taxi Data?
SELECT COUNT(1) FROM <project_id>.ny_taxi.green_taxi_data;
```


### Question 2

**Question:** Count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

**Answer:** 0 MB for the External Table and 6.41MB for the Materialized Table.

```sql
-- Count the distinct number of PULocationIDs for the entire dataset on both the tables
-- External table
SELECT COUNT(DISTINCT PULocationID) FROM <project_id>.ny_taxi.external_green_taxi_data;

-- Materialized table
SELECT COUNT(DISTINCT PULocationID) FROM <project_id>.ny_taxi.green_taxi_data;
```


### Question 3

**Question:** How many records have a fare_amount of 0?

**Answer:** 1,622.


```sql
-- How many records have a fare_amount of 0?
SELECT COUNT(1) FROM <project_id>.ny_taxi.green_taxi_data
WHERE fare_amount = 0;
```


### Question 4

**Question:** What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy).

**Answer:** Partition by lpep_pickup_datetime and Cluster on PUlocationID.


```sql
-- Create a table partitioned by lpep_pickup_datetime and clustered by PUlocationID
CREATE OR REPLACE TABLE <project_id>.ny_taxi.green_taxi_data_partitioned_clustered
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID AS
SELECT * FROM <project_id>.ny_taxi.green_taxi_data;
```


### Question 5

**Question:** Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime
06/01/2022 and 06/30/2022 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? 

**Answer:** 12.82 MB for non-partitioned table and 1.12 MB for the partitioned table.

```sql
-- Non partitioned or clustered table
SELECT DISTINCT (PULocationID) FROM <project_id>.ny_taxi.green_taxi_data
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

-- Partitioned and clustered table
SELECT DISTINCT (PULocationID) FROM <project_id>.ny_taxi.green_taxi_data_partitioned_clustered
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';
```


### Question 6

**Question:** Where is the data stored in the External Table you created?

**Answer:** GCP Bucket.


### Question 7

**Question:** It is best practice in Big Query to always cluster your data.

**Answer:** False.

Clustering may improve performance and lower costs on big datasets for certain types of queries, such as queries that use filter clauses and queries that aggregate data. On the other hand, tables with less than 1GB do not show significant improvement with partitioning and clustering; doing so in a small table could even lead to increased cost due to the additional metadata reads and maintenance needed for these features.



### Question 8

**Question:** Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

**Answer:** 0 bytes. Because BigQuery stores some metadata about materialized table, such as the number of rows, so this query doesn't really need to read or count the records.

```sql
-- Count the number of records
SELECT COUNT(*) FROM <project_id>.ny_taxi.green_taxi_data;
```

