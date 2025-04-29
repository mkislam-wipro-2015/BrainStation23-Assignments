variable "region" {
  default = "ap-southeast-1"
}
variable "vpc_id" {
  default = "vpc-058299fc75736538b"
}
variable "subnet_ids" {
  default = ["subnet-0669d4cdc1c983644", "subnet-010ece5268f761803"]
}
variable "cluster_name" {
  default = "brainstation-eks-cluster"
}
