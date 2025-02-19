import boto3
import csv

def check_iam_roles():
    iam = boto3.client('iam')
    roles = iam.list_roles()['Roles']
    result = []
    
    for role in roles:
        role_name = role['RoleName']
        policies = iam.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
        for policy in policies:
            if policy['PolicyName'] == 'AdministratorAccess':
                result.append([role_name, policy['PolicyName']])
    
    with open('iam_roles_audit.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['IAMRoleName', 'PolicyName'])
        writer.writerows(result)
    print("IAM roles audit completed.")

def check_iam_mfa():
    iam = boto3.client('iam')
    users = iam.list_users()['Users']
    result = []
    
    for user in users:
        user_name = user['UserName']
        mfa_devices = iam.list_mfa_devices(UserName=user_name)['MFADevices']
        mfa_enabled = "True" if mfa_devices else "False"
        result.append([user_name, mfa_enabled])
    
    with open('iam_mfa_audit.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['IAMUserName', 'MFAEnabled'])
        writer.writerows(result)
    print("IAM MFA audit completed.")

def check_security_groups():
    ec2 = boto3.client('ec2')
    security_groups = ec2.describe_security_groups()['SecurityGroups']
    result = []
    
    for sg in security_groups:
        sg_name = sg['GroupName']
        for rule in sg['IpPermissions']:
            for ip_range in rule.get('IpRanges', []):
                if ip_range.get('CidrIp') == '0.0.0.0/0' and rule['FromPort'] in [22, 80, 443]:
                    result.append([sg_name, rule['FromPort'], ip_range['CidrIp']])
    
    with open('security_groups_audit.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['SGName', 'Port', 'AllowedIP'])
        writer.writerows(result)
    print("Security groups audit completed.")

def check_unused_key_pairs():
    ec2 = boto3.client('ec2')
    key_pairs = {kp['KeyName'] for kp in ec2.describe_key_pairs()['KeyPairs']}
    used_keys = set()
    
    instances = ec2.describe_instances()['Reservations']
    for res in instances:
        for inst in res['Instances']:
            if 'KeyName' in inst:
                used_keys.add(inst['KeyName'])
    
    unused_keys = key_pairs - used_keys
    
    with open('unused_key_pairs.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['UnusedKeyPair'])
        writer.writerows([[key] for key in unused_keys])
    print("Unused key pairs audit completed.")

if __name__ == "__main__":
    check_iam_roles()
    check_iam_mfa()
    check_security_groups()
    check_unused_key_pairs()
    print("All security audits completed.")