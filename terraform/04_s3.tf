resource "random_id" "id" {
  byte_length = 3
}

resource "aws_s3_bucket" "dump_bucket" {
  bucket              = "etl-dump-bucket-${random_id.id.hex}"
  force_destroy       = true
  object_lock_enabled = false
  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_s3_bucket_versioning" "dump_bucket_versioning" {
  bucket = aws_s3_bucket.dump_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_acl" "dump_bucket_acl" {
  bucket = aws_s3_bucket.dump_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "s3_encryption" {
  bucket = aws_s3_bucket.dump_bucket.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# resource "aws_s3_bucket_policy" "allow_all_s3" {
#   bucket = aws_s3_bucket.dump_bucket.id
#   policy = data.aws_iam_policy_document.s3_policy.json
# }

# data "aws_iam_policy_document" "s3_policy" {
#   statement {
#     principals {
#       type        = "AWS"
#       identifiers = [aws_iam_user.zappa_user.arn]
#     }

#     actions = [
#       "s3:*"
#     ]

#     resources = [
#       aws_s3_bucket.dump_bucket.arn,
#       "${aws_s3_bucket.dump_bucket.arn}/*",
#     ]
#   }
# }
