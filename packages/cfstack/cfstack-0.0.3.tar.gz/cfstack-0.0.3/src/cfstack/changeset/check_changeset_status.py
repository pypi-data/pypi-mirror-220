
import time
 
def check_changeset_status(client,inputs):
    status  =  "Not Available"
    response = {}
    start_time = time.time()
    try:
        while(1):
            end_time = time.time()
            if end_time-start_time > 10:
                print("Changeset creation timed out")
                break
            response = client.describe_change_set(
                ChangeSetName=inputs["ChangeSetName"],
                StackName=inputs["StackName"]
            )
            if response["ExecutionStatus"] == "AVAILABLE":
                status = "Available"
                break
    except Exception as e:
        print("")
    finally:
        return status,response