import hashlib
import json

def generate_hash(template_checksum, json_stack_parameters):
    # Convert JSON objects to strings
    stack_parameters = json.dumps(json_stack_parameters, sort_keys=True)
    # Concatenate the  strings
    concatenated_str = template_checksum + stack_parameters
    # Generate hash value
    hash = hashlib.md5(concatenated_str.encode()).hexdigest()
    return hash

def calculate_shamap(prod_local):
    for region in prod_local["Stacks"]:
        for stack in prod_local["Stacks"][region]:
            stack_path = prod_local["Stacks"][region][stack]["TemplatePath"]
            stack_parameters = prod_local["Stacks"][region][stack]["Parameters"]
            with open(stack_path, 'rb') as file:
                template_checksum = hashlib.md5(file.read()).hexdigest()
            hash=generate_hash(template_checksum,stack_parameters)
            prod_local["Stacks"][region][stack]["hash"]=hash
    return prod_local
    