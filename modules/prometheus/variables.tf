# modules/prometheus/variables.tf
variable "network" {
  description = "Docker network neve"
  type        = string
}

variable "app_port" {
  description = "Az alkalmazás portja"
  type        = number
  default     = 5000
}