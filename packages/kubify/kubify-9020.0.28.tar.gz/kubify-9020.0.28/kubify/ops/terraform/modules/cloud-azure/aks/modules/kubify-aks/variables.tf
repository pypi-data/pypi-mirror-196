variable "cluster_name" {
  description = "should match the file name envs/[cluster_name].yaml"
}
variable "aks_region" {
  description = "should match the file name envs/[cluster_name].yaml"
  default     = "westus"
}