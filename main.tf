provider "aws" {
  region = "us-east-1"
}

# 1. S3 Bucket for CSV Artifacts
resource "aws_s3_bucket" "product_data_bucket" {
  bucket = "my-product-search-data-bucket-unique-123" # Change this uniqueness
  
  tags = {
    Name = "Product Data Bucket"
    Environment = "Dev"
  }
}

# 2. RDS MySQL Instance
# Note: Storing password in plain text here for simplicity of example. 
# In production, use AWS Secrets Manager or vars.
resource "aws_db_instance" "default" {
  allocated_storage    = 10
  db_name              = "product_search"
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  username             = "admin"
  password             = "Password123!" 
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
  publicly_accessible  = true # For easy local testing connection
}

# 3. IAM Role for Lambda
resource "aws_iam_role" "lambda_exec_role" {
  name = "product_search_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Policy to allow Lambda to log and potentially access RDS (via VPC) or S3
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# 4. Lambda Function
# Assuming a deployment package 'lambda_function_payload.zip' exists
# In reality, you'd need to create this zip with all dependencies (numpy, sentence-transformers, etc.)
# which is likely > 50MB, so you'd probably use a Docker Image instead (Image type).
# Here we define as Zip for the assignment deliverable structure.
resource "aws_lambda_function" "product_search" {
  filename      = "lambda_function_payload.zip"
  function_name = "search_products"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_handler.lambda_handler"
  runtime       = "python3.9"
  timeout       = 30 # Inference can be slow
  memory_size   = 1024 # Model needs RAM

  environment {
    variables = {
      DB_HOST     = aws_db_instance.default.address
      DB_USER     = aws_db_instance.default.username
      DB_PASSWORD = aws_db_instance.default.password
      DB_NAME     = aws_db_instance.default.db_name
    }
  }
}

output "rds_endpoint" {
  value = aws_db_instance.default.endpoint
}

output "s3_bucket_name" {
  value = aws_s3_bucket.product_data_bucket.id
}
