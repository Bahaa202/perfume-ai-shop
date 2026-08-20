variable "aws_region" {
  description = "AWS region to deploy resources in"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type (2GB RAM needed for k3s + Podman + app workloads)"
  type        = string
  default     = "t3.small"
}

variable "key_pair_name" {
  description = "Name of the AWS key pair to use for SSH access"
  type        = string
}

variable "project_name" {
  description = "Name prefix used for tagging resources"
  type        = string
  default     = "perfume-ai-shop"
}
