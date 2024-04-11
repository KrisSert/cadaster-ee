variable "credentials" {
  description = "My Credentials"
  default     = "./keys/gcs_terraform_api_key.json"
}

variable "project" {
  description = "Project in Google Cloud"
  default     = "de-zoomcamp-411619"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bigquery_dataset_name" {
  description = "My BigQuery DataSet Name"
  default     = "CADASTER"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "cadaster_data_bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}