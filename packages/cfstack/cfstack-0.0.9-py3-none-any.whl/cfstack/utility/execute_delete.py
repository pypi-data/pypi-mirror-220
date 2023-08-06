from cfstack.utility.create_client import create_client
from cfstack.changeset.create_changeset import create_changeset
from cfstack.changeset.execute_changeset import execute_changeset
from cfstack.changeset.delete_changeset import delete_changeset
from cfstack.changeset.check_changeset_status import check_changeset_status
from cfstack.stack.check_stack_update_status import check_stack_update_status
from cfstack.stack.delete_stack import delete_stack
from cfstack.stack.check_stack_delete_status import check_stack_delete_status

def execute_delete(stack):
    executed = "Not Deleted"
    print(stack["StackName"]+" will be deleted\n")
    client = create_client(stack["Region"])
    response = delete_stack(client,stack)
    if response != "Stack Deletion Triggered":
        return executed
    status = check_stack_delete_status(client,stack)
    if status == "Deleted":
        executed = "Deleted"                    
    return executed
