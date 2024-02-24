# Convert CSV files from DataTalksClub backup to Parquet

[Video source](https://www.youtube.com/watch?v=CI3P4tAtru4).


In order to minimize errors and discrepancies in the source data formats, we will create a script that downloads the datasets for 2020 and 2021 and parquetizes them with a predefined schema.

We will use the [DataTalksClub backup](https://github.com/DataTalksClub/nyc-tlc-data) to get the original data in CSV format.

* Download the data.
    + We create the [download_data.sh](./download_data.sh) Bash script, and we make it executable via `chmod +x download_data.sh` command.
    + Run the script with the appropriate values for the arguments.
        ```sh
        ./download_data.sh yellow 2020
        ./download_data.sh yellow 2021
        ./download_data.sh green 2020
        ./download_data.sh green 2021
        ```
    + Check one of the file contents to verify the downloading worked as expected.
        ```sh
        zcat ../../data/nyc_tlc/raw/yellow/2021/01/yellow_tripdata_2021_01.csv.gz | head -n 10
        ```

* Parquetize the datasets.
    + Run the [convert_csv_to_parquet.py](./convert_csv_to_parquet.py) Python script.
        ```sh
        python convert_csv_to_parquet.py
        ```
        - The [convert_csv_to_parquet.ipynb](./convert_csv_to_parquet.ipynb) notebook has been used for initial tests before converting the code to the Python script.