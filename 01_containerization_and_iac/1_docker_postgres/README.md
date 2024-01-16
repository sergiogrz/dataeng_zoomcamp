# Docker + Postgres

## Table of contents
* [Python packages required for this section](#python-packages-required-for-this-section).
* [Running Postgres and Pgcli](#running-postgres-and-pgcli).
* [Running Postgres and PgAdmin](#running-postgres-and-pgadmin).
    + Via Docker.
    + Via Docker Compose.
* [Ingesting NY Taxi data to Postgres](#ingesting-ny-taxi-data-to-postgres).
    + Data exploration.
    + Data ingestion pipeline script.
    + Dockerizing the ingestion script.
* [Shutting the services down](#shutting-the-services-down).



## Python packages required for this section

Listed in [environment.yml](./../../environment.yml).

* **Pandas**.
* **Pgcli:** command line interface for Postgres.
* **Psycopg:** Postgres adapter for Pyhton.
* **SQLAlchemy:** Python SQL toolkit.



## Running Postgres and Pgcli

```bash
docker run -d \
    -e POSTGRES_USER=root \
    -e POSTGRES_PASSWORD=root \
    -e POSTGRES_DB=ny_taxi \
    -v ./data/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:15.5
```

In order to see what's inside _ny_taxi_postgres_data_ directory, adjust its permissions of by running `sudo chmod a+rwx ./data/ny_taxi_postgres_data`.


[**Pgcli**](https://www.pgcli.com/) is a command line interface for Postgres.

```bash
pgcli \
    -h localhost \
    -p 5432 \
    -u root \
    -d ny_taxi
```

## Running Postgres and pgAdmin

[**PgAdmin**](https://www.pgadmin.org/) is an open-source GUI management tool for Postgres.


### Via Docker

* Create a network.
    ```bash
    docker network create pg_net
    ```

* Run Postgres.
    ```bash
    docker run -d \
        -e POSTGRES_USER=root \
        -e POSTGRES_PASSWORD=root \
        -e POSTGRES_DB=ny_taxi \
        -v ./data/ny_taxi_postgres_data:/var/lib/postgresql/data \
        -p 5432:5432 \
        --network pg_net \
        --name pg_database \
        postgres:15.5
    ```

* Run pgAdmin.
    ```bash
    docker run -d \
        -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
        -e PGADMIN_DEFAULT_PASSWORD=root \
        -p 8080:80 \
        --network pg_net \
        --name pg_admin \
        dpage/pgadmin4
    ```

You may now login into the pgAdmin web UI at `localhost:8080` and create a connection to the Postgres database (`Add New Server`).



### Via Docker Compose

Instead of running Postgres and pgAdmin, with all their configurations, using two Docker commands, we can make use of Docker Compose, which is a convenient way to run multiple related services with just one configuration file (see [docker-compose.yml](./docker-compose.yml)).

* First, to make pgAdmin configuration persistent, create a folder `pgadmin_data` inside `data`. This folder will be then bind-mounted to the `/var/lib/pgadmin` folder from the pgAdmin container. As indicated in the [pgAdmin documentation](https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html#mapped-files-and-directories), you must change its ownership via `sudo chown 5050:5050 ./data/pgadmin_data`. 

* Next, run Postgres and pgAdmin.
    ```bash
    docker compose up -d
    ```

Once we have our Postgres service running, we can proceed with the next section.



## Ingesting NY Taxi data to Postgres

Throughout the course, we make use of the **NYC Taxi and Limousine Commission dataset**, which can be found [here](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). However, NYC TLC changed the format of the data files to parquet. The CSV files that will be used along the course are accessible [here](https://github.com/DataTalksClub/nyc-tlc-data).


### Data exploration

First, we make use of the notebook [upload_data.ipynb](./upload_data.ipynb) to explore the dataset, create the database schema and write the data to the Postgres database. 



### Data ingestion pipeline script

We have created Python script to automate the data ingestion process, which can be found [here](./ingest_data.py).

Below is the command for running the script with the appropriate arguments, which in this case loads the Yellow Taxi data from January 2021 to our Postgres database.

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table=yellow_taxi_data \
    --url=${URL}
```


### Dockerizing the ingestion script

We use the `ingest_data.py` script that we just created to create Dockerfile (see [ingestion.Dockerfile](./ingestion.Dockerfile)), so that we can build a Docker image with it, by using the following command:

```bash
docker build -f ingestion.Dockerfile -t taxi_ingest:001 .
```

Once the image is built, run the container from the image, using the network we have previously created, and with the name of our Postgres container as the name of the host.

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
    --network pg_net \
    taxi_ingest:001 \
        --user=root \
        --password=root \
        --host=pg_database \
        --port=5432 \
        --db=ny_taxi \
        --table=yellow_taxi_data \
        --url=${URL}
```


## Shutting the services down

To stop and remove the containers and network, run:

```bash
docker compose down
```
 