from cfstack.stack.check_stack_exists import check_stack_exists
from cfstack.changeset.generate_changesetname import generate_changesetname

def create_changeset(client,stack):
    response={}

    response["Status"]="Not Created"
    change_set_type = "UPDATE" if(check_stack_exists(client,stack)=="Stack Exists") else "CREATE"
    if change_set_type == "CREATE":
        print(stack["StackName"]+" does not exist will be created\n")
    else:
        print(stack["StackName"]+" exists will be updated\n")    
    change_set_name = generate_changesetname()
    response["ChangeSetName"] = change_set_name
    response["StackName"] = stack["StackName"]    
    capabilities = ['CAPABILITY_IAM','CAPABILITY_NAMED_IAM','CAPABILITY_AUTO_EXPAND']
    try:
        client.create_change_set(
            StackName=stack["StackName"],
            TemplateURL=stack["TemplateURL"],
            Parameters=stack["Parameters"],
            Capabilities=capabilities,
            ChangeSetName=change_set_name,
            ChangeSetType=change_set_type
        )
        response["Status"]="Created"
    except Exception as e:
        print("")
    finally:
        return response