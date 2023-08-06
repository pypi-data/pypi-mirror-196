

provider "google" {
  region = var.region
}

data "google_client_config" "default" {}

provider "kubernetes" {
  host                   = "https://${module.gke.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
}

module "gke" {
  source     = "../../"
  project_id = var.project_id
  regional   = false
  region     = var.region
  zones      = [var.zone]

  name = "config-sync-cluster${var.cluster_name_suffix}"

  network           = google_compute_network.main.name
  subnetwork        = google_compute_subnetwork.main.name
  ip_range_pods     = google_compute_subnetwork.main.secondary_ip_range[0].range_name
  ip_range_services = google_compute_subnetwork.main.secondary_ip_range[1].range_name

  service_account = "create"
  node_pools = [
    {
      name         = "node-pool"
      autoscaling  = false
      auto_upgrade = true
      node_count   = 4
      machine_type = "e2-standard-4"
    },
  ]
}
