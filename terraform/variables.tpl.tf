
variable "cloud_api_key" {
  description = "Confluent Cloud API Key (also referred as Cloud API ID)"
  type        = string
  default     = "<YOUR VALUE HERE>"
}

variable "cloud_api_secret" {
  description = "Confluent Cloud API Secret"
  type        = string
  sensitive   = true
  default     = "<YOUR VALUE HERE>"
}

variable "environment_id" {
  description = "The ID of the Environment that the Kafka cluster belongs to of the form 'env-'"
  type        = string
  default     = "<YOUR VALUE HERE>"
}

variable "open_api_key" {
  description = "Open API Key"
  type        = string
  sensitive   = true
  default     = "<YOUR VALUE HERE>"
}

variable "topic_name" {
  description = "The name of the Kafka topic to create with default settings"
  default = "reddit"
}

locals {
  data_lake_bucket = "de-zoomcamp-project-bucket"
}

variable "project" {
  description = "Project ID"
  default = "<YOUR VALUE HERE>"
}

variable "credentials" {
  description = "Google cloud credentials file path"
  default = "../google-services.json"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-west6"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that data will be written to"
  type = string
  default = "reputation"
}
