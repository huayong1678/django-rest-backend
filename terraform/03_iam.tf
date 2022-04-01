resource "aws_iam_role" "ecs_host_role" {
  name               = "ECSHostRole"
  path               = "/"
  assume_role_policy = file("policies/ecs-role.json")
}

resource "aws_iam_role" "ecs_service_role" {
  name               = "ECSServiceRole"
  path               = "/"
  assume_role_policy = file("policies/ecs-role.json")
}

resource "aws_iam_policy" "ecs_instance_role_policy" {
  name        = "ECSInstanceRolePolicy"
  description = "ECS Instance Role Policy"
  policy      = file("policies/ecs-instance-role-policy.json")
}

resource "aws_iam_policy" "ecs_service_role_policy" {
  name        = "ECSServiceRolePolicy"
  description = "ECS Service Role Policy"
  policy      = file("policies/ecs-service-role-policy.json")
}

resource "aws_iam_role_policy_attachment" "attach_instance_role" {
  role       = aws_iam_role.ecs_host_role.name
  policy_arn = aws_iam_policy.ecs_instance_role_policy.arn
}

resource "aws_iam_role_policy_attachment" "attach_service_role" {
  role       = aws_iam_role.ecs_service_role.name
  policy_arn = aws_iam_policy.ecs_service_role_policy.arn
}

resource "aws_iam_instance_profile" "ecs" {
  name = "ECSInstanceProfile"
  role = aws_iam_role.ecs_host_role.name
}

resource "aws_iam_role" "glue" {
  name               = "AWSGlueServiceRoleDefault"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "glue.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "glue_s3_policy" {
  name = "my_s3_policy"
  role = aws_iam_role.glue.id
  depends_on = [
    aws_s3_bucket.glue_bucket
  ]
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "arn:aws:s3:::*"
      ]
    }
  ]
}
EOF
}


resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}
resource "aws_iam_role_policy" "glue_service_s3" {
  name   = "glue_service_s3"
  role   = aws_iam_role.glue.id
  policy = aws_iam_role_policy.glue_s3_policy.policy
}
