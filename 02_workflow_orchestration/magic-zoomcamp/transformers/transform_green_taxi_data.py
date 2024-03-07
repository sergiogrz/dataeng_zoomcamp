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
