# variable "credentials" {
#   description = "Your credentials."
#   default     = "~/.google/credentials/google_credentials.json"
# }

variable "project" {
  description = "Project ID."
  default     = "warm-rock-411419"
}

variable "region" {
  description = "Region for your project."
  default     = "europe-west1-b"
}

variable "location" {
  description = "Project location."
  default     = "EU"
}

variable "gcs_bucket_name" {
  description = "Your Google Cloud Storage bucket name."
  default     = "warm-rock-411419-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Storage class type for your bucket."
  default     = "STANDARD"
}

variable "bq_dataset_name" {
  description = "Your BigQuery dataset name."
  default     = "demo_dataset"
}
