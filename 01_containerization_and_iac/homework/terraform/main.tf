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
  # credentials = file(var.credentials)
  project = var.project
  region  = var.region
}

resource "google_storage_bucket" "dataeng_zoomcamp_bucket" {
  name          = "${local.gcs_bucket}_${var.project}"
  location      = var.location
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

resource "google_bigquery_dataset" "dataeng_zoomcamp_dataset" {
  dataset_id = var.bq_dataset_name
  # Project: if not specified, the provider project is used
  # project    = "<your Project ID>"
  location = var.location
}
