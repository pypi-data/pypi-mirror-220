import boto3
def delete_changeset(client,inputs):   
    deleted = "Execution Failed"
    try:
        client.delete_change_set(
            ChangeSetName=inputs["ChangeSetName"],
            StackName=inputs["StackName"],
        )
        deleted = "Deleted"
    except Exception as e:
        print("Deleting Changeset - ",e)
    finally:
        return deleted