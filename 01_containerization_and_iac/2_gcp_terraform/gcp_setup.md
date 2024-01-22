# GCP setup

Once we have our Google Cloud account (see [Prerequisites](README.md#prerequisites)):

1. Create a Google Cloud [project](https://developers.google.com/workspace/guides/create-project).
2. Create a service account for this project. A [service account](https://cloud.google.com/iam/docs/service-account-overview) is a special kind of account typically used by an application or compute workload rather than a person.
    * `IAM and admin` > `Service accounts` > `Create a service account`.
    * Service account name: _dataeng-zoomcamp-user_.
    * Grant roles (this can be modified via `IAM and admin` > `IAM` > `Permission`):
        + Storage Admin, to work with Google Cloud Storage.
        + BigQuery Admin, to work with BigQuery.
        + Compute Admin, to work with Compute Engine.
3. Create a [service account key](https://cloud.google.com/iam/docs/keys-create-delete#creating). This is used to establish the identity of the service account, so that we can use it from outside of Google Cloud.
    * From the service accounts panel: `Actions` > `Manage keys` > `Add key` > `Create new key`.
    * Key type: JSON.
4. The JSON file containing the key will be downloaded to your computer. Save it in a path of your choice (I save it as `~/.google/credentials/google_credentials.json`).
5. Download and install the Google Cloud CLI following the [documentation](https://cloud.google.com/sdk/docs/install-sdk#deb) for local setup.
6. Set environment variable to point to your downloaded GCP keys:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
   ```
7. Refresh token/session and verify authentication
   ```bash
   gcloud auth application-default login
   ```

If everything works as expected you will get a notification in a new window confirming that you have successfully authenticated with the gcloud CLI. You should now be ready to work with GCP.