output "ecr_repository_url" {
  description = "ECR repository to push the application image to."
  value       = aws_ecr_repository.app.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name."
  value       = aws_ecs_cluster.app.name
}

output "ecs_service_name" {
  description = "ECS web service name."
  value       = aws_ecs_service.web.name
}

output "ecs_task_definition_arn" {
  description = "Task definition ARN used for the app and one-off migration task."
  value       = aws_ecs_task_definition.web.arn
}

output "public_subnet_ids" {
  description = "Public subnet IDs used by the ALB and restricted Fargate tasks."
  value       = aws_subnet.public[*].id
}

output "web_security_group_id" {
  description = "Task security group for the one-off migration task."
  value       = aws_security_group.web.id
}

output "load_balancer_dns_name" {
  description = "Set the DNS record for the application hostname to this ALB."
  value       = aws_lb.app.dns_name
}

output "database_endpoint" {
  description = "Private RDS endpoint; reachable only from the web task security group."
  value       = aws_db_instance.database.address
}

output "application_secret_arn" {
  description = "Secrets Manager secret ARN containing SECRET_KEY and DATABASE_URL."
  value       = aws_secretsmanager_secret.application.arn
}
