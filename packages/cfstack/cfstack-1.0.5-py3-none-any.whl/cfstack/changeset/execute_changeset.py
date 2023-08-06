import boto3
def execute_changeset(client,inputs):   
    executed = "Execution Failed"
    try:
        client.execute_change_set(
            ChangeSetName=inputs["ChangeSetName"],
            StackName=inputs["StackName"],
        )
        executed = "Executed"
    except Exception as e:
        print("Executing Changeset - ",e)
    finally:
        return executed