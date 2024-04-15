terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.12.0"
    }
  }
}

provider "google" {
  # Configuration options
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}


resource "google_storage_bucket" "GCS_Bucket" {
  name          = var.gcs_bucket_name
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

# Mage service account & api key
resource "google_service_account" "mage-service-account" {
  account_id   = "mage-service-account"
  display_name = "Mage Service Account"
}
resource "google_project_iam_binding" "mage-service-acc-iam-binding" {
  project = var.project
  role    = "roles/editor"

  members = [
    "serviceAccount:${google_service_account.mage-service-account.email}"
  ]
}

# DBT service account & api key
resource "google_service_account" "dbt-service-account" {
  account_id   = "dbt-service-account"
  display_name = "DBT Service Account"
}
resource "google_project_iam_binding" "dbt-service-acc-iam-binding" {
  project = var.project
  role    = "roles/bigquery.admin"

  members = [
    "serviceAccount:${google_service_account.dbt-service-account.email}"
  ]
}
resource "google_project_iam_binding" "dbt-service-acc-iam-binding-2" {
  project = var.project
  role    = "roles/storage.admin"
  members = [
    "serviceAccount:${google_service_account.dbt-service-account.email}",
  ]
}