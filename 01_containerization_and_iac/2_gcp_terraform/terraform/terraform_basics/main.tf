terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.12.0"
    }
  }
}

provider "google" {
  # Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
  # credentials = file("<path to your credentials file>")
  project = "warm-rock-411419"
  region  = "europe-west1-b"
}

resource "google_storage_bucket" "demo_bucket" {
  name          = "warm-rock-411419-terra-bucket"
  location      = "EU"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = "demo_dataset"
  # Project: if not specified, the provider project is used
  # project    = "<your Project ID>"
  location = "EU"
}
