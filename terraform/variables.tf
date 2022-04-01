# Input variable definitions

variable "infra_name" {
  type    = string
  default = "etl-"
}

variable "aws_region" {
  description = "AWS region for all resources."

  type    = string
  default = "us-east-1"
}

# networking

variable "public_subnet_1_cidr" {
  description = "CIDR Block for Public Subnet 1"
  default     = "10.1.1.0/24"
}
variable "public_subnet_2_cidr" {
  description = "CIDR Block for Public Subnet 2"
  default     = "10.1.2.0/24"
}
variable "private_subnet_1_cidr" {
  description = "CIDR Block for Private Subnet 1"
  default     = "10.1.3.0/24"
}
variable "private_subnet_2_cidr" {
  description = "CIDR Block for Private Subnet 2"
  default     = "10.1.4.0/24"
}
variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

# RDS
variable "rds_spec" {
  description = "RDS Information use input when deploy."
  type = object({
    allocated_storage   = number
    storage_type        = string
    engine              = string
    engine_version      = string
    instance_class      = string
    publicly_accessible = bool
    availability_zone   = string
    multi_az            = bool
    port                = number
  })
  default = {
    allocated_storage   = 20
    availability_zone   = "us-east-1a"
    engine              = "postgres"
    engine_version      = "11"
    instance_class      = "db.t2.micro"
    multi_az            = false
    publicly_accessible = true
    storage_type        = "gp2"
    port                = 5432
  }
}

variable "rds_db_name" {
  description = "DB_NAME *SENSITIVE*"
  type        = string
  sensitive   = true
}
variable "rds_username" {
  description = "USERNAME *SENSITIVE*"
  type        = string
  sensitive   = true
}
variable "rds_password" {
  description = "PASSWORD *SENSITIVE*"
  type        = string
  sensitive   = true
}