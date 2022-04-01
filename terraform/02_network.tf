resource "aws_vpc" "vpc" {
  cidr_block           = "10.1.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = format("%s%s", var.infra_name, "vpc")
  }
}

resource "aws_default_security_group" "vpc_default_security_group" {
  vpc_id = aws_vpc.vpc.id

  ingress {
    protocol  = -1
    from_port = 0
    to_port   = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = format("%s%s", var.infra_name, "vpc-default-sg")
  }
}

# Public subnets
resource "aws_subnet" "public-subnet-1" {
  cidr_block        = var.public_subnet_1_cidr
  vpc_id            = aws_vpc.vpc.id
  availability_zone = var.availability_zones[0]
  tags = {
    Name = format("%s%s", var.infra_name, "public-subnet-1")
  }
}
resource "aws_subnet" "public-subnet-2" {
  cidr_block        = var.public_subnet_2_cidr
  vpc_id            = aws_vpc.vpc.id
  availability_zone = var.availability_zones[1]
  tags = {
    Name = format("%s%s", var.infra_name, "public-subnet-2")
  }
}

# Private subnets
resource "aws_subnet" "private-subnet-1" {
  cidr_block        = var.private_subnet_1_cidr
  vpc_id            = aws_vpc.vpc.id
  availability_zone = var.availability_zones[0]
  tags = {
    Name = format("%s%s", var.infra_name, "private-subnet-1")
  }
}
resource "aws_subnet" "private-subnet-2" {
  cidr_block        = var.private_subnet_2_cidr
  vpc_id            = aws_vpc.vpc.id
  availability_zone = var.availability_zones[1]
  tags = {
    Name = format("%s%s", var.infra_name, "private-subnet-2")
  }
}

# Route tables for the subnets
resource "aws_route_table" "public-route-table" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = format("%s%s", var.infra_name, "public-route-table")
  }
}
resource "aws_route_table" "private-route-table" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = format("%s%s", var.infra_name, "private-route-table")
  }
}

# Associate the newly created route tables to the subnets
resource "aws_route_table_association" "public-route-1-association" {
  route_table_id = aws_route_table.public-route-table.id
  subnet_id      = aws_subnet.public-subnet-1.id
}
resource "aws_route_table_association" "public-route-2-association" {
  route_table_id = aws_route_table.public-route-table.id
  subnet_id      = aws_subnet.public-subnet-2.id
}
resource "aws_route_table_association" "private-route-1-association" {
  route_table_id = aws_route_table.private-route-table.id
  subnet_id      = aws_subnet.private-subnet-1.id
}
resource "aws_route_table_association" "private-route-2-association" {
  route_table_id = aws_route_table.private-route-table.id
  subnet_id      = aws_subnet.private-subnet-2.id
}

# Elastic IP
resource "aws_eip" "elastic-ip-for-nat-gw" {
  vpc                       = true
  associate_with_private_ip = "10.1.0.5"
  depends_on                = [aws_internet_gateway.igw]
}

# NAT gateway
resource "aws_nat_gateway" "nat-gw" {
  allocation_id = aws_eip.elastic-ip-for-nat-gw.id
  subnet_id     = aws_subnet.public-subnet-1.id
  depends_on    = [aws_eip.elastic-ip-for-nat-gw]
  tags = {
    Name = format("%s%s", var.infra_name, "nat-gw")
  }
}
resource "aws_route" "nat-gw-route" {
  route_table_id         = aws_route_table.private-route-table.id
  nat_gateway_id         = aws_nat_gateway.nat-gw.id
  destination_cidr_block = "0.0.0.0/0"
}

# Internet Gateway for the public subnet
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = format("%s%s", var.infra_name, "igw")
  }
}

# Route the public subnet traffic through the Internet Gateway
resource "aws_route" "public-internet-igw-route" {
  route_table_id         = aws_route_table.public-route-table.id
  gateway_id             = aws_internet_gateway.igw.id
  destination_cidr_block = "0.0.0.0/0"
}

#Private Subnet Security Groups
resource "aws_security_group" "private-sg" {
  name        = "private-subnet-sg"
  description = "Allow TCP 5432 from Public Subnet"
  vpc_id      = aws_vpc.vpc.id
  tags = {
    Name = format("%s%s", var.infra_name, "private-subnet-sg")
  }

  # ingress {
  #   from_port       = 5432
  #   to_port         = 5432
  #   protocol        = "tcp"
  #   security_groups = [aws_security_group.public-sg.id]
  # }

  # ingress {
  #   from_port       = 80
  #   to_port         = 80
  #   protocol        = "tcp"
  #   security_groups = [aws_security_group.public-sg.id]
  # }

    ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.public-sg.id]
  }

  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.public-sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

#Public Subnet Security Groups
resource "aws_security_group" "public-sg" {
  name        = "public-subnet-sg"
  description = "Allow HTTP and HTTPS from Internet"
  vpc_id      = aws_vpc.vpc.id
  tags = {
    Name = format("%s%s", var.infra_name, "public-subnet-sg")
  }


  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 433
    to_port     = 433
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}