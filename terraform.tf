resource "aws_instance" "vulnerable_instance" {
  ami           = "ami-xxxxxxxx" # Replace with a valid, but potentially outdated, AMI ID
  instance_type = "t2.micro"
  key_name      = "insecure_key" # Assuming an insecure or easily compromised key pair exists

  # Insecure Security Group allowing broad access
  vpc_security_group_ids = [aws_security_group.insecure_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              # Intentionally insecure user data
              echo "This server is intentionally vulnerable!" > /tmp/vulnerable.txt
              sudo yum update -y # Potentially pulling in outdated packages
              sudo yum install -y httpd # Installing a common web server
              sudo systemctl start httpd
              # BAD PRACTICE: Directly writing sensitive info to a file
              echo "DATABASE_PASSWORD=SuperSecret123" > /var/www/html/config.txt
              EOF

  tags = {
    Name = "VulnerableInstance"
  }
}

resource "aws_security_group" "insecure_sg" {
  name_prefix = "insecure-sg-"
  vpc_id      = "vpc-yyyyyyyy" # Replace with a valid VPC ID

  # Insecure rule: Allowing all inbound traffic from anywhere
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # All protocols
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Insecure rule: Allowing all outbound traffic to anywhere (usually default, but explicitly shown)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "InsecureSecurityGroup"
  }
}

# Assuming an insecure or easily compromised key pair is used
resource "aws_key_pair" "insecure_key_pair" {
  key_name   = "insecure_key"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD3b...example...publicKey... user@example.com" # Replace with a weak or publicly known key
}
