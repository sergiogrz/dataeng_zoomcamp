# Module 2 - Workflow orchestration

> Course video sources: videos `2.2.x` from the [DE Zoomcamp playlist](https://www.youtube.com/watch?v=Li8-MWHhTbo&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb).


## Table of contents

* [What will we build?](#what-will-we-build).
* [Intro to orchestration](#intro-to-orchestration).
* [Intro to Mage](#intro-to-mage).
    + What is Mage?.
    + Mage setup.
    + Configuring Postgres.
* [ETL: API to Postgres](#etl-api-to-postgres).
    + Data loader.
    + Transformer.
    + Data exporter.




## What will we build?

<img src="../images/02_mage_project_diagram.png" alt="mage project diagram" style="width: 60%; height: auto;">

**Extract:** pull data from a source (API - NYC dataset).  
**Transform:** data cleaning, transformation, and partitioning.  
**Load:** API to Mage, Mage to Postgres, GCS, BigQuery.


## Intro to orchestration

Resources: [Slides](https://docs.google.com/presentation/d/17zSxG5Z-tidmgY-9l7Al1cPmz4Slh4VPK6o2sryFYvw).

A large part of data engineering is **extracting**, **transforming**, and **loading** data between sources. **Orchestration** is a process of dependency management, facilitated through **automation**. The data orchestrator manages scheduling, triggering, monitoring, and even resource allocation.

Every workflow requires sequential steps:
* Steps = tasks.
* Workflows = DAGs.

![data engineering lifecycle](../images/02_data_engineering_lifecycle.png)

As one of the undercurrents, orchestration is key to the entire process of building data engineering pipelines.

**A good orchestrator handles:**
* Workflow management.
* Automation.
* Error handling.
* Recovery.
* Monitoring, alerting.
* Resource optimization.
* Observability.
* Debugging.
* Compliance/auditing.



## Intro to Mage

Resources:
* [Getting started repo](https://github.com/mage-ai/mage-zoomcamp).
* [Slides](https://docs.google.com/presentation/d/1y_5p3sxr6Xh1RqE6N8o2280gUzAdiic2hPhYUUD6l88).


### What is Mage?

[Mage](https://www.mage.ai/) is an open-source pipeline tool for orchestrating, transforming, and integrating data.


**Main concepts in Mage:**
* **Project** 
    + It forms the basis for all the work you can do in Mage; like a repository on GitHub.
    + It contains all the code for all of your pipelines, blocks, and other assets.
    + A Mage instance has one or more projects.
* **Pipeline**
    + Workflow that executes some data operation; also called DAGs on other platforms.
    + Contains references to all the blocks of code you want to run (written in SQL, Python, or R), charts for visualizing data, and organizes the dependency between each block of code.
    + Each pipeline is represented by a YAML file in the _pipelines_ folder of your project.
* **Block:** 
    + A file with code that can be executed independently or within a pipeline. Commonly in data engineering we use blocks to export, transform, and load data.
    + Together, blocks form pipelines (DAGs).
    + A block won't start running in a pipeline until all its upstream dependencies are met.


<img src="../images/02_mage_core_concepts.png" alt="mage core concepts" style="width: 50%; height: auto;">


Visit the [docs page](https://docs.mage.ai/introduction/overview) to find more information on these and other Mage concepts.



### Mage setup

For this section we make use of the [Mage Getting started repo](https://github.com/mage-ai/mage-zoomcamp/tree/master). Instead of cloning it and creating a new repository, we download the project files, and copy those we need. These starting files are:
* Dockerfile.
* Docker compose file.
* requirements.txt.
* dev.env

Copy `dev.env` as `.env`.


(Build, if necessary, and) start the container.
```bash
docker compose up -d
```

Now, navigate to `localhost:6789` in your browser to access Mage UI.


**Mage repository structure**  
We just initialized a new mage repository. It will be present in your project under the name `magic-zoomcamp`. If you changed the varable `PROJECT_NAME` in the `.env` file, it will be named whatever you set it to.

This repository should have the following structure:

```
.
├── mage_data
│   └── magic-zoomcamp
├── magic-zoomcamp
│   ├── __pycache__
│   ├── charts
│   ├── custom
│   ├── data_exporters
│   ├── data_loaders
│   ├── dbt
│   ├── extensions
│   ├── interactions
│   ├── pipelines
│   ├── scratchpads
│   ├── transformers
│   ├── utils
│   ├── __init__.py
│   ├── io_config.yaml
│   ├── metadata.yaml
│   └── requirements.txt
├── Dockerfile
├── README.md
├── dev.env
├── .env
├── docker-compose.yml
└── requirements.txt
```


In order to be able to see and modify files out of the Mage UI (for example, in VSCode), change the ownership of `magic-zoomcamp` and `mage_data` directories.
```bash
sudo chown -R <your-user>:<your-group> magic-zoomcamp mage_data
```


### Configuring Postgres

In this section, we configure a Postgres client in Mage to connect to a local Postgres database, which exists in a Docker container (started along with Mage via Docker Compose).

In order to connect Mage with that Postgres instance, edit the `io_config.yaml` file (inside `magic-zoomcamp` directory). This file is where we manage our connections.

There, create a new connection profile, `dev` (useful, for example, for separating dev and production environment), and add your Postgres credentials. Mage uses [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) templating and `env_var()` function to interpolate environment variables.

```yml
dev:
  # PostgresSQL
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: "{{ env_var('POSTGRES_DBNAME') }}"
  POSTGRES_SCHEMA: "{{ env_var('POSTGRES_SCHEMA') }}"
  POSTGRES_USER: "{{ env_var('POSTGRES_USER') }}"
  POSTGRES_PASSWORD: "{{ env_var('POSTGRES_PASSWORD') }}"
  POSTGRES_HOST: "{{ env_var('POSTGRES_HOST') }}"
  POSTGRES_PORT: "{{ env_var('POSTGRES_PORT') }}"
```

Once Postgres is configured, we can check if the connection is successful by creating a `test_postgres` SQL data loader with the query `SELECT 1;`. If it returns a 1 after a "Postgres initialized" message, then the connection to our Postgres local instance is well established.



## ETL: API to Postgres

We are going to load data from an API that takes the form of a compressed CSV file to our local Postgres database. Our pipeline will pull data, perform a light transformation, and write it to the database.

In the UI, start a new batch pipeline, and rename it as `api_to_postgres`.


### Data loader

To create a new data loader, use the API template and name the block `load_api_data`.

In this example, we use the [NY Yellow Taxi dataset](https://github.com/DataTalksClub/nyc-tlc-data) from January 2021.

There, you need to map data types to process the dataset more efficiently. To see the schema and what data types to expect, you can make use of the [upload_data.ipynb notebook](../01_containerization_and_iac/1_docker_postgres/upload_data.ipynb) from module 1. Also, as we did in the previous module, make sure `tpep_pickup_datetime` and `tpep_dropoff_datetime` columns are loaded in date format.

After applying the appropriate changes, the data loader (and its template test function) looks like is shown below.

```py
import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'

    taxi_dtypes = {
        "VendorId": pd.Int64Dtype(),
        "passenger_count": pd.Int64Dtype(),
        "trip_distance": float,
        "RatecodeID": pd.Int64Dtype(),
        "store_and_fwd_flag": str,
        "PULocationID": pd.Int64Dtype(),
        "DOLocationID": pd.Int64Dtype(),
        "payment_type": pd.Int64Dtype(),
        "fare_amount": float,
        "extra": float,
        "mta_tax": float,
        "tip_amount": float,
        "tolls_amount": float,
        "improvement_surcharge": float,
        "total_amount": float,
        "congestion_surcharge": float
    }

    # native date parsing
    parse_dates_cols = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]

    return pd.read_csv(
        url,
        sep=",",
        dtype=taxi_dtypes,
        parse_dates=parse_dates_cols,
        compression="gzip"
    )


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
```


### Transformer

Next, add a transformer using the generic Python template, and name the block `transform_taxi_data`. This transformer will remove records with value 0 for `passenger_count`. In addition, add a test to check that there are no rides with zero passengers after the transformation is done.

Below is the block of code for this transformer.

```py
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    print(f"Records with zero passengers: {len(data[data['passenger_count'] == 0])}")

    return data[data["passenger_count"] > 0]


@test
def test_output(output, *args) -> None:
    assert not any(output['passenger_count'] == 0), "There are rides with zero passengers!"
```


### Data exporter

Last step, add a data exporter using the PostgreSQL template. Name it as `taxi_data_to_postgres`.

There, modify the value of these variables: `schema_name`, `table_name`, and `config_profile`, as shown below.

```py
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = "ny_taxi"  # Specify the name of the schema to export data to
    table_name = "yellow_taxi_data"  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = "dev"

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  # Specifies whether to include index in exported table
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
```


As in [Configuring Postgres](#configuring-postgres) section, you can create a SQL data loader just to check if the data has been correctly loaded (for example with a `SELECT * FROM ny_taxi.yellow_taxi_data LIMIT 10;` query).
SELECT * FROM ny_taxi.yellow_taxi_data LIMIT 10;

