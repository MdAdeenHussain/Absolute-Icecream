variable "aws_region" {
  description = "AWS region for the deployment and ACM certificate."
  type        = string
}

variable "project_name" {
  description = "Short lowercase identifier used in resource names."
  type        = string
  default     = "absolute-icecream"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,24}$", var.project_name))
    error_message = "project_name must be 3-25 lowercase letters, digits, or hyphens and start with a letter."
  }
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "production"
}

variable "vpc_cidr" {
  description = "CIDR range for the deployment VPC."
  type        = string
  default     = "10.40.0.0/16"
}

variable "certificate_arn" {
  description = "ACM certificate ARN for the public HTTPS hostname, in aws_region."
  type        = string
}

variable "db_name" {
  description = "PostgreSQL database name."
  type        = string
  default     = "absolute_icecream"
}

variable "db_username" {
  description = "Dedicated application database username; password is generated and stored in Secrets Manager."
  type        = string
  default     = "absolute_app"

  validation {
    condition     = can(regex("^[A-Za-z][A-Za-z0-9_]{0,30}$", var.db_username))
    error_message = "db_username must begin with a letter and contain only letters, digits, and underscores."
  }
}

variable "db_instance_class" {
  description = "RDS PostgreSQL instance size. Choose a class available in the selected region."
  type        = string
  default     = "db.t4g.micro"
}

variable "db_allocated_storage" {
  description = "Initial encrypted RDS storage in GiB."
  type        = number
  default     = 20
}

variable "db_max_allocated_storage" {
  description = "Maximum autoscaled RDS storage in GiB."
  type        = number
  default     = 100
}

variable "db_deletion_protection" {
  description = "Protect the production database from accidental deletion. Disable only for a planned teardown."
  type        = bool
  default     = true
}

variable "app_image_tag" {
  description = "Immutable image tag to deploy; prefer a source-control commit SHA."
  type        = string
  default     = "latest"
}

variable "desired_count" {
  description = "Number of web tasks. Start at 0 until the image is pushed and the database is migrated."
  type        = number
  default     = 0
}

variable "task_cpu" {
  description = "Fargate task CPU units."
  type        = number
  default     = 512
}

variable "task_memory" {
  description = "Fargate task memory in MiB."
  type        = number
  default     = 1024
}

variable "log_retention_days" {
  description = "CloudWatch log retention."
  type        = number
  default     = 30
}
