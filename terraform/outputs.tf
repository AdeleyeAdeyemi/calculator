output "public_ip" {
  value = aws_instance.ec2.public_ip
}

output "private_key_path" {
  value = local_file.private_key.filename
}

