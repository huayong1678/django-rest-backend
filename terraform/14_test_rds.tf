# Public RDS
resource "aws_db_instance" "dest_database" {
  identifier              = format("%s%s", var.infra_name, "dest-rds")
  allocated_storage       = var.rds_spec.allocated_storage
  storage_type            = var.rds_spec.storage_type
  engine                  = var.rds_spec.engine
  engine_version          = var.rds_spec.engine_version
  instance_class          = var.rds_spec.instance_class
  db_name                 = var.rds_db_name_dest
  username                = var.rds_username_dest
  password                = var.rds_password_dest
  port                    = var.rds_spec.port
  publicly_accessible     = var.rds_spec.publicly_accessible
  availability_zone       = var.rds_spec.availability_zone
  multi_az                = var.rds_spec.multi_az
  backup_retention_period = 0
  # backup_window              = "10:05-10:35"
  # maintenance_window         = "sun:07:47-sun:08:17"
  auto_minor_version_upgrade = false
  copy_tags_to_snapshot      = true
  skip_final_snapshot        = true
  apply_immediately          = true
  delete_automated_backups   = true
  deletion_protection        = false
  depends_on = [
    aws_vpc.production-vpc,
    aws_subnet.public-subnet-1,
    aws_subnet.public-subnet-2,
  ]
  db_subnet_group_name   = aws_db_subnet_group.database_subnet.name
  vpc_security_group_ids = [aws_default_security_group.vpc_default_security_group.id]
}

resource "aws_db_instance" "source_database" {
  identifier              = format("%s%s", var.infra_name, "source-rds")
  allocated_storage       = var.rds_spec.allocated_storage
  storage_type            = var.rds_spec.storage_type
  engine                  = var.rds_spec.engine
  engine_version          = var.rds_spec.engine_version
  instance_class          = var.rds_spec.instance_class
  db_name                 = var.rds_db_name_source
  username                = var.rds_username_source
  password                = var.rds_password_source
  port                    = var.rds_spec.port
  publicly_accessible     = var.rds_spec.publicly_accessible
  availability_zone       = var.rds_spec.availability_zone
  multi_az                = var.rds_spec.multi_az
  backup_retention_period = 0
  # backup_window              = "10:05-10:35"
  # maintenance_window         = "sun:07:47-sun:08:17"
  auto_minor_version_upgrade = false
  copy_tags_to_snapshot      = true
  skip_final_snapshot        = true
  apply_immediately          = true
  delete_automated_backups   = true
  deletion_protection        = false
  depends_on = [
    aws_vpc.production-vpc,
    aws_subnet.public-subnet-1,
    aws_subnet.public-subnet-2,
    aws_db_subnet_group.database_subnet,
  ]
  db_subnet_group_name   = aws_db_subnet_group.database_subnet.name
  vpc_security_group_ids = [aws_default_security_group.vpc_default_security_group.id]
}

resource "aws_db_subnet_group" "database_subnet" {
  name_prefix = "test-db-subnet-"
  subnet_ids  = [aws_subnet.public-subnet-1.id, aws_subnet.public-subnet-2.id]
  tags = {
    Name = format("%s%s", var.infra_name, "rds-sg")
  }
}

variable "infra_name" {
  type    = string
  default = "etl-"
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

variable "rds_db_name_source" {
  description = "Source => DB_NAME *SENSITIVE*"
  type        = string
  sensitive   = true
}
variable "rds_username_source" {
  description = "Source => USERNAME *SENSITIVE*"
  type        = string
  sensitive   = true
}
variable "rds_password_source" {
  description = "Source => PASSWORD *SENSITIVE*"
  type        = string
  sensitive   = true
}

variable "rds_db_name_dest" {
  description = "Destination => DB_NAME *SENSITIVE*"
  type        = string
  sensitive   = true
}
variable "rds_username_dest" {
  description = "Destination => USERNAME *SENSITIVE*"
  type        = string
  sensitive   = true
}
variable "rds_password_dest" {
  description = "Destination => PASSWORD *SENSITIVE*"
  type        = string
  sensitive   = true
}
