# modules/python_app/variables.tf
variable "container_name" {
  description = "A Docker konténer neve"
  type        = string
}

variable "app_port" {
  description = "Az alkalmazás portja"
  type        = number
  default     = 5000
}

variable "image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}

variable "container_count" {
  description = "Indítandó konténerek száma"
  type        = number
  default     = 4
}

variable "memory_limit" {
  description = "Memória limit MB-ban"
  type        = number
  default     = 256  # 256 MB
}

variable "restart_policy" {
  description = "Újraindítási szabály"
  type        = string
  default     = "unless-stopped"  # always, on-failure, unless-stopped
}

variable "healthcheck" {
  description = "Healthcheck beállítások"
  type = object({
    enabled      = bool
    test         = list(string)
    interval     = string
    timeout      = string
    retries      = number
    start_period = string
  })
  default = {
    enabled      = true
    test         = ["CMD", "curl", "-f", "http://localhost:5000"]
    interval     = "30s"
    timeout      = "10s"
    retries      = 3
    start_period = "40s"
  }
}

# Új változó a hálózathoz
variable "network" {
  description = "Docker hálózat neve"
  type        = string
  default     = "devops-network"
}
