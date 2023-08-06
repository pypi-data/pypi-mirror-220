import boto3
def delete_stack(client,stack):
    stack_deleted = "Stack Deletion Couldn't be Triggered"
    try:
        client.delete_stack(
            StackName=stack["StackName"]
        )
        stack_deleted = "Stack Deletion Triggered"
    except Exception as e:
        print(e)
        stack_deleted = "Stack Deletion Couldn't be Triggered"
    finally:
        return stack_deleted