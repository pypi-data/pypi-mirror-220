import boto3

def create_client(shamap_region):   
    client = boto3.client('s3',region_name=shamap_region)
    return client