# variables.tf
variable "project_name" {
  description = "A projekt neve, ami az erőforrások elnevezésében is megjelenik"
  type        = string
  default     = "devops"
}

variable "environment" {
  description = "Környezet neve (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "python_app_port" {
  description = "Az alkalmazás portja"
  type        = number
  default     = 5000
}

variable "mysql_root_password" {
  description = "MySQL root jelszó"
  type        = string
  sensitive   = true
}

variable "zabbix_mysql_password" {
  description = "Zabbix MySQL felhasználó jelszava"
  type        = string
  sensitive   = true
}

variable "graylog_password_secret" {
  description = "Graylog password secret"
  type        = string
  sensitive   = true
}

variable "graylog_root_password_sha2" {
  description = "Graylog root jelszó SHA-256 hash-e"
  type        = string
  sensitive   = true
}
