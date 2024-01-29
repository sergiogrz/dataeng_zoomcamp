# Module 2 Homework Solutions

## Setup

Before proceeding with the module homework, we must ensure we meet the following requirements, as it's been explained in the module videos:
* A Mage service up ([Mage setup](../README.md#mage-setup)).
* Postgres configuration ([Configuring Postgres](../README.md#configuring-postgres)).
* GCP configuration ([Configuring GCP](../README.md#configuring-gcp)).


## Assignment

### Data loader

I parameterize the data loader block by creating two global variables: `years` and `months`, which are passed via the `**kwargs` parameter in the block function. These variables are both lists with the values we're interested in:
* years = [2020]
* months = [10, 11, 12]

The data loader function is presented below.

```py
@data_loader
def load_data_from_api(*args, **kwargs):
    base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green"
    years = kwargs["years"]
    months = kwargs["months"]
    urls = [f"{base_url}/green_tripdata_{year}-{month:02d}.csv.gz" for year in years for month in months]

    taxi_dtypes = {
        "VendorId": pd.Int64Dtype(),
        "store_and_fwd_flag": str,
        "RatecodeID": pd.Int64Dtype(),
        "PULocationID": pd.Int64Dtype(),
        "DOLocationID": pd.Int64Dtype(),
        "passenger_count": pd.Int64Dtype(),
        "trip_distance": float,
        "fare_amount": float,   
        "extra": float,
        "mta_tax": float,
        "tip_amount": float,
        "tolls_amount": float,
        "ehail_fee": float,
        "improvement_surcharge": float,
        "total_amount": float,
        "payment_type": pd.Int64Dtype(),
        "trip_type": pd.Int64Dtype(),
        "congestion_surcharge": float
    }

    # native date parsing
    parse_dates_cols = ["lpep_pickup_datetime", "lpep_dropoff_datetime"]

    # empty initial DataFrame
    df = pd.DataFrame()

    # iterate over the URLs
    for url in urls:
        # try to read the CSV file from the URL
        try:
            new_df = pd.read_csv(
                url,
                sep=",",
                dtype=taxi_dtypes,
                parse_dates=parse_dates_cols,
                compression="gzip"
            )
        except Exception as e:
            print(f"Could not read CSV file from {url}: {e}")
            continue
        
        # concatenate the new DataFrame with the existing DataFrame if there's one
        if not df.empty:
            df = pd.concat([df, new_df], ignore_index=True)
        else:
            df = new_df

    return df
```


### Transformer

Script for the transformer function and tests:

```py
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    # check existing values of VendorID
    print(f"Existing values of column 'VendorID': {df['VendorID'].unique()}")
    # remove rows with value 0 for passenger_count or trip_distance
    print("Before transformation:")
    print(f"Records with zero passengers: {len(df[df['passenger_count'] == 0])}")
    print(f"Records with no trip distance: {len(df[df['trip_distance'] == 0])}")
    nrecords_before = len(df)

    df = df[(df["passenger_count"] > 0) & (df["trip_distance"] > 0)]
    nrecords_after = len(df)

    print("After transformation:")
    print(f"Number of deleted records: {nrecords_before - nrecords_after}")

    # create a lpep_pickup_date column
    df["lpep_pickup_date"] = df["lpep_pickup_datetime"].dt.date

    # rename columns in camel case to snake case
    column_mapping = {
        "VendorID": "vendor_id",
        "RatecodeID": "ratecode_id",
        "PULocationID": "pulocation_id",
        "DOLocationID": "dolocation_id",
    }
    df.rename(columns=column_mapping, inplace=True)

    return df

@test
def test_passenger_count(output, *args) -> None:
    assert not any(output["passenger_count"] == 0), "There are rides with zero passengers!"

@test
def test_trip_distance(output, *args) -> None:
    assert not any(output["trip_distance"] == 0), "There are rides with no trip distance!"

@test
def test_vendor_id_exists(output, *args) -> None:
    assert "vendor_id" in output.columns, "There is no column named 'vendor_id'"
```



### Postgres Data exporter

In this case, I use the Python PostgreSQL template. Inside, I just modify the value for the following varibles (the rest remains unchanged):
* schema_name = "mage"
* table_name = "green_taxi"
* config_profile = "dev"

In order to check that the data has been correctly loaded, I create a new SQL data loader where I run the query `SELECT * FROM mage.green_taxi LIMIT 10;`.



### GCS Data exporter

Script for the data exporter:

```py
import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/src/google_credentials_mage.json"
bucket_name = '<bucket name>'
project_id = '<project id>'
table_name = 'green_taxi_data'
root_path = f"{bucket_name}/{table_name}"

@data_exporter
def export_data(data, *args, **kwargs):
    table = pa.Table.from_pandas(data)
    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table=table,
        root_path=root_path,
        partition_cols=["lpep_pickup_date"],
        filesystem=gcs,
    )
```

Once it's executed, the table `green_taxi_data` partitioned by date will be created in the specified GCS bucket.


## Questions

### Question 1. Data Loading

**Question:** Once the dataset is loaded, what's the shape of the data?

**Answer:** 266,855 rows x 20 columns.


### Question 2. Data Transformation

**Question:** Upon filtering the dataset where the passenger count is equal to 0 _or_ the trip distance is equal to zero, how many rows are left?

**Answer:** 139,370 rows.


### Question 3. Data Transformation

**Question:** Which of the following creates a new column `lpep_pickup_date` by converting `lpep_pickup_datetime` to a date?

**Answer:** data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date.


### Question 4. Data Transformation

**Question:** What are the existing values of `VendorID` in the dataset?

**Answer:** 1 or 2.


### Question 5. Data Transformation

**Question:** How many columns need to be renamed to snake case?

**Answer:** 4.


### Question 6. Data Exporting

**Question:** Once exported, how many partitions (folders) are present in Google Cloud?

**Answer:** 95.