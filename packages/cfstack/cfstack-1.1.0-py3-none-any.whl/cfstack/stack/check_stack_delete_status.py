import boto3
import time
 
def check_stack_delete_status(client,stack):
    status = "Unknown"
    start = time.time()
    try:
        while(1):
            end = time.time()
            if end-start > 60:
                print("Stack delete check timed out")
                status = "Unknown"
                break
            response = client.describe_stacks(
                StackName=stack["StackName"]
            )
            if response["Stacks"][0]["StackStatus"] in  ['CREATE_FAILED','CREATE_COMPLETE','ROLLBACK_FAILED','ROLLBACK_COMPLETE','DELETE_FAILED','DELETE_COMPLETE','UPDATE_COMPLETE','UPDATE_FAILED','UPDATE_ROLLBACK_FAILED','UPDATE_ROLLBACK_COMPLETE','IMPORT_COMPLETE','IMPORT_ROLLBACK_FAILED','IMPORT_ROLLBACK_COMPLETE']:
                status = response["Stacks"][0]["StackStatus"]
                break
    except Exception as e:   
        if "does not exist" in str(e):
            status = "DELETE_COMPLETE"
    finally:
        delete_status = "Deleted" if (status in ['DELETE_COMPLETE'])  else "Not Deleted"
        return delete_status