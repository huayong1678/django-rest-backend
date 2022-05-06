resource "aws_instance" "BASTION" {
  ami                    = "ami-0022f774911c1d690"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public-subnet-1.id
  vpc_security_group_ids = [aws_security_group.load-balancer.id]
  key_name               = "etl-backend-ecs"
  tags = {
    Name = "bastionhost"
  }
  lifecycle {
    ignore_changes = all
  }
}
