terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = "your-gcp-project-id"
  region  = "us-central1"
}

resource "google_container_cluster" "primary" {
  name     = "vector-server-cluster"
  location = "us-central1"
  # Add other configurations as needed
}

# Add other resources as needed (e.g., Google Kubernetes Engine node pools, networking configurations)
