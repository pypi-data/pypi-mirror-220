from cfstack.utility.execute_deploy import execute_deploy
from cfstack.utility.parameter_preprocessing import parameter_preprocessing
from cfstack.s3utility.upload_file_s3 import upload_file_s3
from cfstack.s3utility.delete_file_s3 import delete_file_s3
import json
from cfstack.s3utility.create_client import create_client
from cfstack.utility.create_client import create_client as create_clientcf
from cfstack.utility.calculate_shamap import calculate_shamap
from cfstack.utility.compare_shamap import compare_shamap
from cfstack.stack.delete_stack import delete_stack
def first_time_upload():
    # Upload First Time Prod.json to S3
    with open("prod.json", "r") as json_file:
        prod_json = json.load(json_file)
    bucket_name = prod_json["BucketName"]
    bucket_region = prod_json["BucketRegion"]
    s3client=create_client(bucket_region)
    prod_file_details={
        "BucketName":bucket_name,
        "FilePath":"prod.json",
        "Key":"prod.json"   
    }
    upload_file_s3(s3client,prod_file_details)
    
    # Upload all the stack templates First Time to S3
    for region in prod_json["Regions"]:
        stack_region = region["Name"]
        for stack in region["Stacks"]:
            stack_name = stack["Name"]
            stack_file_details = {
                "FilePath":stack["TemplatePath"],   
                "BucketName":bucket_name,
                "Key":stack["TemplatePath"].split("/")[-1]
            }
            upload_file_s3(s3client,stack_file_details)
            
    # Upload SHAMap.json FirstTime to S3  
    shamap=calculate_shamap(prod_json)
    with open("shamap.json", "w") as json_file:
        json.dump(shamap, json_file)
    shamap_file_details={
        "BucketName":bucket_name,
        "FilePath":"shamap.json",
        "Key":"shamap.json"   
    }
    file_upload_status=upload_file_s3(s3client,shamap_file_details)
    first_time_upload=False
    if file_upload_status=="File Uploaded":
        first_time_upload=True