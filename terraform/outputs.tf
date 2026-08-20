output "instance_public_ip" {
  description = "Elastic IP address of the EC2 instance (stays fixed across stop/start)"
  value       = aws_eip.app_eip.public_ip
}

output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_server.id
}
