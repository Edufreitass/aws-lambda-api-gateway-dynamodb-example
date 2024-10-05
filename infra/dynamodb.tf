resource "aws_dynamodb_table" "example_table" {
  name         = "tb_example"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "PK"

  attribute {
    name = "PK"
    type = "S"
  }
}
