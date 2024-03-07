import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

dtypes_yellow = {
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

parse_dates_yellow = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]

dtypes_green = {
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

parse_dates_green = ["lpep_pickup_datetime", "lpep_dropoff_datetime"]

dtypes_fhv = {
        "dispatching_base_num": str,
        "PUlocationID": pd.Int64Dtype(),
        "DOlocationID": pd.Int64Dtype(),
        "SR_Flag": float,
        "Affiliated_base_number": str
    }

parse_dates_fhv = ["pickup_datetime", "dropOff_datetime"]

dtypes = {
    "yellow": [dtypes_yellow, parse_dates_yellow],
    "green": [dtypes_green, parse_dates_green],
    "fhv": [dtypes_fhv, parse_dates_fhv]
}


@data_loader
def load_data_from_api(*args, **kwargs):
    base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"
    service = kwargs["service"]
    year = kwargs["year"]
    month = kwargs["month"]
    url = f"{base_url}{service}/{service}_tripdata_{year}-{month:02}.csv.gz"
    


    return pd.read_csv(
        url,
        sep=",",
        dtype=dtypes[service][0],
        parse_dates=dtypes[service][1],
        compression="gzip"
    )


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
