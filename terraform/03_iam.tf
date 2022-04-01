resource "aws_iam_role" "ecs_host_role" {
  name = "ECSHostRole"
  path = "/"
  assume_role_policy = file("policies/ecs-role.json")
}

resource "aws_iam_role" "ecs_service_role" {
  name = "ECSServiceRole"
  path = "/"
  assume_role_policy = file("policies/ecs-role.json")
}

resource "aws_iam_policy" "ecs_instance_role_policy" {
  name        = "ECSInstanceRolePolicy"
  description = "ECS Instance Role Policy"
  policy = file("policies/ecs-instance-role-policy.json")
}

resource "aws_iam_policy" "ecs_service_role_policy" {
  name        = "ECSServiceRolePolicy"
  description = "ECS Service Role Policy"
  policy = file("policies/ecs-service-role-policy.json")
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