from cfstack.utility.create_client import create_client
from cfstack.changeset.create_changeset import create_changeset
from cfstack.changeset.execute_changeset import execute_changeset
from cfstack.changeset.delete_changeset import delete_changeset
from cfstack.changeset.check_changeset_status import check_changeset_status
from cfstack.stack.check_stack_update_status import check_stack_update_status
from tabulate import tabulate

def execute_deploy(stack):
    executed = "Not Deployed"

    client = create_client(stack["Region"])
    
    response = create_changeset(client,stack)
    if response["Status"] == "Not Created": 
        return executed
    
    status,response = check_changeset_status(client,response)
    if status != "Available":
        delete_changeset(client,response)
        return executed                     
    
    print("\n*****************"+stack["StackName"]+"**********************\n")
    changes=[]
    for change in response["Changes"]:
        if "Replacement" in change["ResourceChange"]:
            changes.append([change["ResourceChange"]["Action"],change["ResourceChange"]["LogicalResourceId"],change["ResourceChange"]["ResourceType"],change["ResourceChange"]["Replacement"]])
        else:
            changes.append([change["ResourceChange"]["Action"],change["ResourceChange"]["LogicalResourceId"],change["ResourceChange"]["ResourceType"],""])
    print(tabulate(changes, headers=["Action", "Logical Id", "Type", "Replacement"]))

    response_exec = execute_changeset(client,response)
    if response_exec != "Executed":
        delete_changeset(client,response)
        return executed
    
   
    status = check_stack_update_status(client,stack)
    if status == "Updated":
        delete_changeset(client,response)
        executed = "Deployed"                    
    return executed