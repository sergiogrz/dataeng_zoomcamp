# Data Engineering Zoomcamp 2024

[Link](https://github.com/DataTalksClub/data-engineering-zoomcamp) to the course.

Taught by [DataTalksClub](https://github.com/DataTalksClub).


## Requirements

* System requirements (and version used)
    + Docker (v24.0.7).
    + Docker Compose (v2.21.0).
    + Python (v3.9).
    + Google Cloud CLI (v460.0.0).
    + Terraform (v1.7.0).
    + Java (OpenJDK v1.8.0).
    + Spark (v3.3.3).

* Python package requirements: listed in [environment.yml](./environment.yml).

In order to avoid packages and dependencies conflicts, it is recommended to work in an isolated virtual environment.

```bash
conda env create -f environment.yml --force
conda activate dataeng_zc
```


## Course structure

* [Module 1 - Containerization and Infrastructure as Code](./01_containerization_and_iac/).
* [Module 2 - Workflow orchestration](./02_workflow_orchestration/).
* [Workshop 1 - Data ingestion](./workshop_data_ingestion/).
* [Module 3 - Data Warehouse](./03_data_warehouse/).
* [Module 4 - Analytics engineering](./04_analytics_engineering/).
* [Module 5 - Batch processing](./05_batch_processing/).
* Module 6 - Streaming.
* Workshop 2 - Stream processing with SQL.
* Project.


## Extras

* [Load parquet files from NYC TLC record data website to GCS](./extras/load_parquet_files_from_web_to_gcs/).
* [Convert CSV files from DataTalksClub backup to Parquet](./extras/convert_csv_to_parquet/).



## Overview

<img src="./images/overview_diagram.jpg" alt="overview diagram">
