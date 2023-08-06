from cfstack.utility.execute_deploy import execute_deploy
from cfstack.utility.execute_delete import execute_delete
from cfstack.utility.parameter_preprocessing import parameter_preprocessing
from cfstack.s3utility.upload_file_s3 import upload_file_s3
from cfstack.s3utility.delete_file_s3 import delete_file_s3
import json
from cfstack.s3utility.create_client import create_client as create_s3client
from cfstack.utility.create_client import create_client as create_cfclient
from cfstack.utility.calculate_shamap import calculate_shamap
from cfstack.utility.compare_shamap import compare_shamap
from cfstack.stack.delete_stack import delete_stack

def execute():    
    
    
    # Step 1
    with open("prod.json", "r") as json_file:
        prod_local = json.load(json_file)
    bucket_name = prod_local["BucketName"]
    bucket_region = prod_local["BucketRegion"]
    prod_calc=calculate_shamap(prod_local)
    s3client = create_s3client(bucket_region)

    # Step 2
    prod_s3 = {}
    try:
        response=s3client.get_object(Bucket=bucket_name,Key="prod.json")
        prod_s3 = json.loads(response["Body"].read())
    except Exception as e:
        prod_s3 = {
            "BucketName":bucket_name,
            "BucketRegion":bucket_region,
            "Parallel":prod_calc["Parallel"],
            "Stacks":{}
        }

    # Step 3
    for region in prod_calc["Stacks"]:
        for stack in prod_calc["Stacks"][region]:
            stack_path = prod_calc["Stacks"][region][stack]["TemplatePath"]
            stack_file_details = {
                "FilePath":stack_path,   
                "BucketName":bucket_name,
                "Key":stack_path.split("/")[-1]
            }
            upload_file_s3(s3client,stack_file_details,True)
 
       
    
    # Step 4
    different_stacks,todelete_stacks=compare_shamap(prod_s3,prod_calc)
    should_s3prod_be_updated = False
    for region in different_stacks["Stacks"]:
        for stack in different_stacks["Stacks"][region]:
            if different_stacks["Stacks"][region][stack]["SkipUpdate"]:
                if not (stack in prod_s3["Stacks"][region]):
                    del prod_calc["Stacks"][region][stack]
                else:
                    prod_calc["Stacks"][region][stack]=prod_s3["Stacks"][region][stack]
                continue
            stack_path = different_stacks["Stacks"][region][stack]["TemplatePath"]
            stack_parameters = different_stacks["Stacks"][region][stack]["Parameters"]
            stack_details={"Region":region,"StackName":stack,"TemplateURL":f"https://{bucket_name}.s3.{bucket_region}.amazonaws.com/{stack_path.split('/')[-1]}","Parameters":parameter_preprocessing(stack_parameters)}
            status=execute_deploy(stack_details)
            if status == "Deployed":
                stack_file_details = {
                    "FilePath":different_stacks["Stacks"][region][stack]["TemplatePath"],   
                    "BucketName":bucket_name,
                    "Key":"templates-prod/"+stack_path.split('/')[-1]
                }
                should_s3prod_be_updated = True
                upload_file_s3(s3client,stack_file_details,True)
                print("✅ "+stack + " "+status+"\n")  
            else:
                print("❌ "+stack + " "+status+"\n")  
    

    # Step 5
    for region in todelete_stacks["Stacks"]:
        for stack in todelete_stacks["Stacks"][region]:
            stack_path = todelete_stacks["Stacks"][region][stack]["TemplatePath"]
            stack_parameters = todelete_stacks["Stacks"][region][stack]["Parameters"]
            stack_details={"Region":region,"StackName":stack,"TemplateURL":f"https://{bucket_name}.s3.{bucket_region}.amazonaws.com/{stack_path.split('/')[-1]}","Parameters":parameter_preprocessing(stack_parameters)}
            status=execute_delete(stack_details)
            if status == "Deleted":
                stack_file_prod_details = {
                    "FilePath":todelete_stacks["Stacks"][region][stack]["TemplatePath"],   
                    "BucketName":bucket_name,
                    "Key":"templates-prod/"+stack_path.split('/')[-1]
                }
                stack_file_details = {
                    "FilePath":todelete_stacks["Stacks"][region][stack]["TemplatePath"],   
                    "BucketName":bucket_name,
                    "Key":stack_path.split('/')[-1]
                }
                should_s3prod_be_updated = True
                delete_file_s3(s3client,stack_file_details)
                delete_file_s3(s3client,stack_file_prod_details)
                print("✅ "+stack + " "+status+"\n")    
            else:
                print("❌ "+stack + " "+status+"\n")


    # Step 6
    if should_s3prod_be_updated:
        with open('prod_calc.json', 'w') as outfile:
            json.dump(prod_calc, outfile)
        prod_file_details={
            "BucketName":bucket_name,
            "FilePath":"prod_calc.json",
            "Key":"prod.json"   
        }
        upload_file_s3(s3client,prod_file_details,True)
    else:
        print("No changes in any stack")
    