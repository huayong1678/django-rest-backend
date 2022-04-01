# resource "aws_db_instance" "database" {
#   identifier              = format("%s%s", var.infra_name, "rds")
#   allocated_storage       = var.rds_spec.allocated_storage
#   storage_type            = var.rds_spec.storage_type
#   engine                  = var.rds_spec.engine
#   engine_version          = var.rds_spec.engine_version
#   instance_class          = var.rds_spec.instance_class
#   db_name                 = var.rds_db_name
#   username                = var.rds_username
#   password                = var.rds_password
#   port                    = var.rds_spec.port
#   publicly_accessible     = var.rds_spec.publicly_accessible
#   availability_zone       = var.rds_spec.availability_zone
#   multi_az                = var.rds_spec.multi_az
#   backup_retention_period = 0
#   # backup_window              = "10:05-10:35"
#   # maintenance_window         = "sun:07:47-sun:08:17"
#   auto_minor_version_upgrade = false
#   copy_tags_to_snapshot      = true
#   skip_final_snapshot        = true
#   apply_immediately          = true
#   delete_automated_backups   = true
#   deletion_protection        = false
#   depends_on = [
#     aws_vpc.vpc,
#     aws_subnet.private-subnet-1,
#     aws_subnet.private-subnet-2,
#   ]
#   db_subnet_group_name   = aws_db_subnet_group.database_subnet.name
#   vpc_security_group_ids = [aws_default_security_group.vpc_default_security_group.id]
# }

# resource "aws_db_subnet_group" "database_subnet" {
#   name_prefix = "db-subnet-"
#   subnet_ids  = [aws_subnet.private-subnet-1.id, aws_subnet.private-subnet-2.id]
#   tags = {
#     Name = format("%s%s", var.infra_name, "rds-sg")
#   }
# }

# Public RDS

resource "aws_db_instance" "database" {
  identifier              = format("%s%s", var.infra_name, "rds")
  allocated_storage       = var.rds_spec.allocated_storage
  storage_type            = var.rds_spec.storage_type
  engine                  = var.rds_spec.engine
  engine_version          = var.rds_spec.engine_version
  instance_class          = var.rds_spec.instance_class
  db_name                 = var.rds_db_name
  username                = var.rds_username
  password                = var.rds_password
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
    aws_vpc.vpc,
    aws_subnet.public-subnet-1,
    aws_subnet.public-subnet-2,
  ]
  db_subnet_group_name   = aws_db_subnet_group.database_subnet.name
  vpc_security_group_ids = [aws_default_security_group.vpc_default_security_group.id]
}

resource "aws_db_subnet_group" "database_subnet" {
  name_prefix = "db-subnet-"
  subnet_ids  = [aws_subnet.public-subnet-1.id, aws_subnet.public-subnet-2.id]
  tags = {
    Name = format("%s%s", var.infra_name, "rds-sg")
  }
}
