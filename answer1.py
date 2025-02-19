import boto3
import csv

ec2 = boto3.client("ec2")


regions = [region["RegionName"] for region in ec2.describe_regions()["Regions"]]


data = []

for region in regions:
    ec2_region = boto3.client("ec2", region_name=region)
    paginator = ec2_region.get_paginator("describe_instance_type_offerings")
    
    instance_types = set()  
    for page in paginator.paginate(LocationType='region'):
        for instance in page["InstanceTypeOfferings"]:
            instance_types.add(instance["InstanceType"])

    
    for instance_type in instance_types:
        data.append((region, instance_type))


with open("ec2_instance_types.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["region", "instance_type"])  
    writer.writerows(data)  

print("CSV file generated: ec2_instance_types.csv")