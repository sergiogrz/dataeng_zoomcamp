# Creating a GCP infrastructure with Terraform

Reference: [Terraform tutorial- GCP](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started).

## Table of contents
* [Setup](#setup).
    + Terraform basics.
        - a) Google provider.
        - b) Resources.
    + Terraform with variables.
* [Execution](#execution).



## Setup

### Terraform basics

The Terraform files for this introductory part can be found [here](./terraform_basics/).


#### a) Google provider

The provider is the piece of code that Terraform is going to use to talk to GCP, for which we also need the credentials.

We create a `main.tf` file inside our Terraform directory. There, we need to configure our GCP Provider, which can be found in the [Terraform docs](https://registry.terraform.io/providers/hashicorp/google/latest/docs).

We copy the structure of this provider and we update it to our case.

In case we hadn't set `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to our credentials JSON file (which we have done in the [GCP setup](../gcp_setup.md), point 6), we would need to add a value for `credentials` inside `main.tf`.

```tf
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
  project = "<your project ID>"
  region  = "europe-west1-b"
}

```

After this basic configuration we can already run `terraform init` to get the provider.



#### b) Resources

For this example, we are going to create basic **Google Cloud Storage bucket** and **Google BigQuery dataset** resources.

The GCS bucket configuration for Terraform can be found [here](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket). We can use one of the blocks of code there, adapted to out example.

```tf
resource "google_storage_bucket" "<bucket local name>" {
name          = "<bucket name>"
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
```

We add a Google BigQuery Dataset, using as base configuration one of the examples found in the [documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset).

```tf
resource "google_bigquery_dataset" "dataset local name" {
  dataset_id = "<dataset name or ID>"
  # Project: if not specified, the provider project is used
  # project    = "<your Project ID>"
  location = "EU"
}
```


We can see the configuration of what Terraform is going to create by executing `terraform plan`.

In order to deploy our resources, we run `terraform apply`. This creates a `terraform.tfstate` file, which contains information regarding these resources. We can also see them in the [Google Cloud UI](https://console.cloud.google.com/).

To get rid of them, we execute `terraform destroy`. This modifies the contents of `terraform.tfstate`, which now has no resources, and creates a backup file.



### Terraform with variables

The Terraform files for this part can be found [here](./terraform_with_variables/).

Depending on what you're trying to build out using variables is very handy. By convention in Terraform, we're going to create a `variables.tf` file, and then we will use the variables defined there in our other files.

Use the [documentation](https://developer.hashicorp.com/terraform/language/values) as a reference.

Basic `variable` structure inside `variables.tf`:

```tf
variable "gcs_storage_class" {
  description = "Storage class type for your bucket."
  default     = "STANDARD"
}
```

Once the files are ready, we can again use the commands to plan, apply and destroy the resources.


## Execution

```bash
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init
```
```bash
# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"
```
```bash
# Create new infra
terraform apply -var="project=<your-gcp-project-id>"
```
```bash
# Delete infra after your work, to avoid costs on any running services
terraform destroy
```