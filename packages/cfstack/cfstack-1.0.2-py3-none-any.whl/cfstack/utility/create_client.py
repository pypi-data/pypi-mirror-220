import boto3

def create_client(stack_region):   
    client = boto3.client('cloudformation',region_name=stack_region)
    return client