# Load parquet files from NYC TLC record data website to GCS

Quick hack to load Parquet files directly from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page to GCS, without using an orchestrator. 


## Folder structure

```
.
├── nyc_tlc_eda.ipynb       # notebook to explore the shemas of yellow, green and fhv datasets
├── nyc_tlc_web_to_gcs.py   # script to load the Parquet files from the web to GCS
├── README.md               # this document
├── rename_cols.yml         # config file to rename camel case columns as snake case in the datasets
├── schema.yml              # config file to specify the schema of the datasets
```


## Steps

1. Prerequisites: install _pyarrow_  and _google-cloud-storage_ Python libraries (listed in [environment.yml](../environment.yml)).
2. Set environment variables.
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"  # "/home/sgrodriguez/.google/credentials/google_credentials.json"
    export GCP_GCS_BUCKET="<your bucket name>"
    ```
3. Refresh token/session and verify authentication
    ```bash
    gcloud auth application-default login
    ```
4. Execute the script with the desired arguments for _service_ ("yellow", "green", "fhv"), _year_, and _months_ (optional, indicate the months separated by spaces; if you don't specify it, it will consider the 12 months).
    ```bash
    python nyc_tlc_web_to_gcs.py \
        --service yellow \
        --year 2019 \
        --months 1 2
    ```