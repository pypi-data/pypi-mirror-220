import boto3
import time
 
def check_stack_update_status(client,stack):
    status = "Not Available"
    start = time.time()
    try:
        while(1):
            end = time.time()
            if end-start > 180:
                print("Stack update check timed out")
                status = "Unknown"
                break
            response = client.describe_stacks(
                StackName=stack["StackName"]
            )
            if response["Stacks"][0]["StackStatus"] in  ['CREATE_FAILED','CREATE_COMPLETE','ROLLBACK_FAILED','ROLLBACK_COMPLETE','DELETE_FAILED','DELETE_COMPLETE','UPDATE_COMPLETE','UPDATE_FAILED','UPDATE_ROLLBACK_FAILED','UPDATE_ROLLBACK_COMPLETE','IMPORT_COMPLETE','IMPORT_ROLLBACK_FAILED','IMPORT_ROLLBACK_COMPLETE']:
                status = response["Stacks"][0]["StackStatus"]
                break
    except Exception as e:   
        print("Stack status - ",e)
    finally:
        update_status = "Updated" if (status in ['CREATE_COMPLETE','UPDATE_COMPLETE'])  else "Not Updated"
        return update_status