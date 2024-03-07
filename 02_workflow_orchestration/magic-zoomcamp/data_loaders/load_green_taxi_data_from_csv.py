import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


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


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
