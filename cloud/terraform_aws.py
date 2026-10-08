from .interfaces import TerraformGenerator

class AWSTerraformGenerator(TerraformGenerator):
    """Generates AWS Terraform HCL configs."""
    
    def generate_vpc(self, name: str, cidr_block: str) -> str:
        return f"""
resource "aws_vpc" "{name}" {{
  cidr_block           = "{cidr_block}"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {{
    Name = "{name}"
    ManagedBy = "ferrox-iac"
  }}
}}

resource "aws_internet_gateway" "{name}_igw" {{
  vpc_id = aws_vpc.{name}.id
  tags = {{
    Name = "{name}-igw"
  }}
}}
"""

    def generate_database(self, name: str, engine: str, version: str, instance_class: str) -> str:
        return f"""
resource "aws_db_instance" "{name}" {{
  identifier           = "{name}"
  allocated_storage    = 20
  engine               = "{engine}"
  engine_version       = "{version}"
  instance_class       = "{instance_class}"
  username             = "ferrox_admin"
  password             = random_password.db_password.result
  parameter_group_name = "default.{engine}{version.split('.')[0]}"
  skip_final_snapshot  = true
  publicly_accessible  = false

  tags = {{
    ManagedBy = "ferrox-iac"
  }}
}}

resource "random_password" "db_password" {{
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{{}}<>:?"
}}
"""
