import boto3
def check_stack_exists(client,stack):
    stack_exists = "Stack Doesn't Exist"
    response = {}
    try:
        response = client.describe_stacks(
            StackName=stack["StackName"] 
        )
    except Exception as e:
        stack_exists = "Stack Doesn't Exist"
    finally:
        if response and response["Stacks"]:
            stack_exists =  "Stack Exists" if len(response["Stacks"])==1 else "Stack Doesn't Exist"
        return stack_exists