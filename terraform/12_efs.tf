resource "aws_efs_file_system" "ecs-efs" {
  tags = {
    "Name" = "ECS-EFS"
  }
}

resource "aws_efs_mount_target" "mount-subnet-1" {
  file_system_id = aws_efs_file_system.ecs-efs.id
  subnet_id = aws_subnet.private-subnet-1.id
  security_groups = [ aws_security_group.ecs.id ]
}
resource "aws_efs_mount_target" "mount-subnet-2" {
  file_system_id = aws_efs_file_system.ecs-efs.id
  subnet_id = aws_subnet.private-subnet-2.id
  security_groups = [ aws_security_group.ecs.id ]
}