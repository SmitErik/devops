# main.tf
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

# Közös hálózat létrehozása
resource "docker_network" "app_network" {
  name = "${var.project_name}-network"
  driver = "bridge"
  # Enable IPv6 if needed
  ipam_config {
    subnet = "172.100.0.0/16"  # Customize subnet as needed
    gateway = "172.100.0.1"
  }
  internal = false
}

# Python alkalmazás modul
module "python_app" {
  source = "./modules/python_app"
  
  app_port = var.python_app_port
  container_name = "${var.project_name}_python_app"
  network = docker_network.app_network.name

  depends_on = [docker_network.app_network]
}

# Prometheus modul
module "prometheus" {
  source = "./modules/prometheus"
  
  network = docker_network.app_network.name
}

# Grafana modul
module "grafana" {
  source = "./modules/grafana"
  
  network = docker_network.app_network.name
  prometheus_url = "http://prometheus:9090"
}

# Zabbix modul
module "zabbix" {
  source = "./modules/zabbix"
  
  network = docker_network.app_network.name
  mysql_root_password = var.mysql_root_password
  zabbix_mysql_password = var.zabbix_mysql_password
}

# Graylog modul
module "graylog" {
  source = "./modules/graylog"
  
  network                    = docker_network.app_network.name
  graylog_password_secret    = var.graylog_password_secret
  graylog_root_password_sha2 = var.graylog_root_password_sha2
}

output "network_info" {
  value = {
    network_id   = docker_network.app_network.id
    network_name = docker_network.app_network.name
  }
}
