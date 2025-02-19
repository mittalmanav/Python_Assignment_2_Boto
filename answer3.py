import boto3

def get_billed_regions():
   
    ec2_client = boto3.client("ec2")

    
    all_regions = [region["RegionName"] for region in ec2_client.describe_regions()["Regions"]]
    active_regions = []

    
    for region in all_regions:
        ec2 = boto3.client("ec2", region_name=region)
        instances = ec2.describe_instances()

        
        if instances["Reservations"]:
            active_regions.append(region)

    return active_regions


billed_regions = get_billed_regions()
print("Billed AWS Regions:", billed_regions)