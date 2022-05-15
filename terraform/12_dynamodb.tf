resource "aws_dynamodb_table" "transforms" {
  name = "Transforms"
  read_capacity = 1
  write_capacity = 1
  hash_key = "UUID"
  attribute {
    name = "UUID"
    type = "S"
  }
}