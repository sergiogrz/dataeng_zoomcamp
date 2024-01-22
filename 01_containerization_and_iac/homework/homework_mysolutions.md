# Module 1 Homework Solutions

> **NOTE** 
> The queries used to answer the SQL questions can also be found in the [sql_queries.sql](./sql_queries.sql) script.

## Question 1. Knowing Docker tags

**Question:** Which tag has the following text? - _Automatically remove the container when it exits_

**Answer:** `--rm`.

```bash
docker run --help
```


## Question 2. Understanding docker first run

**Question:** Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash. Now check the python modules that are installed (use `pip list`). What is version of the package _wheel_ ?

**Answer:** `0.42.0`.

```bash
docker run -it \
    --entrypoint /bin/bash \
    --rm \
    python:3.9

# once inside the docker container
pip list
```

## Prepare Postgres

* Set up Postgres and PgAdmin with Docker Compose (follow [Running Postgres and pgAdmin via Docker Compose](../1_docker_postgres/README.md#via-docker-compose)).

* Download taxi zones data and ingest it to Postgres using a [Python script](./ingest_taxi_zones_data.py) (via Pandas and SQLAlchemy):
    ```bash
    python ingest_taxi_zones_data.py
    ```

* Green Taxi trips data from September 2019.
    + Download and explore the dataset (see [explore_data.ipynb](./explore_data.ipynb)).
    + Ingest data using a [Docker image](./ingestion.Dockerfile) from a [Python script](./ingest_data.py), which is a slightly modified version of the  one from the [Docker + Postgres section](../1_docker_postgres/ingest_data.py), to be able to ingest data from both Yellow and Green Taxi datasets (since these have different column names).
        ```bash
        # build the Docker image
        docker build -f ingestion.Dockerfile -t taxi_ingest:002 .

        # run the container from the image
        URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

        docker run -it \
            --network pg_net \
            taxi_ingest:002 \
                --user=root \
                --password=root \
                --host=pg_database \
                --port=5432 \
                --db=ny_taxi \
                --table=green_taxi_data \
                --url=${URL}
        ```


## Question 3. Count records 

**Question:** How many taxi trips were totally made on September 18th 2019?

**Answer:** 15612.

```sql
select count(*) from green_taxi_data
where date(lpep_pickup_datetime) = '2019-09-18'
and date(lpep_dropoff_datetime) = '2019-09-18';
```


## Question 4. Largest trip for each day

**Question:** Which was the pick up day with the largest trip distance?

**Answer:** 2019-09-26.

```sql
select 
	date(lpep_pickup_datetime) as pickup_date,
	max(trip_distance) as max_trip_distance
from green_taxi_data
where date(lpep_pickup_datetime) between '2019-09-01' and '2019-09-30'
group by pickup_date
order by max_trip_distance desc;
```


## Question 5. Three biggest pick up Boroughs

**Question:** Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown. Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

**Answer:** Brooklyn, Manhattan, and Queens.

```sql
select
	z."Borough" as borough,
	sum(gt.total_amount) as sum_total_amount
from green_taxi_data as gt
inner join taxi_zones as z
on gt."PULocationID" = z."LocationID"
where date(lpep_pickup_datetime) = '2019-09-18'
and z."Borough" != 'Unknown'
group by borough
having sum(gt.total_amount) > 50000
order by sum_total_amount desc;
```


## Question 6. Largest tip

**Question:** For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?

**Answer:** JFK Airport.

```sql
select
	zpu."Zone" as pickup_zone,
	zdo."Zone" as dropoff_zone,
	max(gt.tip_amount) as max_tip
from green_taxi_data as gt
inner join taxi_zones as zpu
on gt."PULocationID" = zpu."LocationID"
left join taxi_zones as zdo
on gt."DOLocationID" = zdo."LocationID"
where date(gt.lpep_pickup_datetime) between '2019-09-01' and '2019-09-30'
and zpu."Zone" = 'Astoria'
group by pickup_zone, dropoff_zone
order by max_tip desc;
```


## Terraform

The `main.tf` and `variables.tf` files used to deploy the infrastructure can be found [here](./terraform/).


## Question 7. Creating Resources

**Question:** Run `terraform apply` and paste the output of this command into the homework submission form.

Execution steps (to run inside `terraform` folder):

```bash
gcloud auth application-default login

terraform init

terraform plan 

terraform apply
```


**Answer:**

```bash
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataeng_zoomcamp_dataset: Creating...
google_storage_bucket.dataeng_zoomcamp_bucket: Creating...
google_storage_bucket.dataeng_zoomcamp_bucket: Creation complete after 2s [id=<GCS bucket ID>]
google_bigquery_dataset.dataeng_zoomcamp_dataset: Creation complete after 2s [id=projects/<project ID>/datasets/<BQ dataset name>]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```