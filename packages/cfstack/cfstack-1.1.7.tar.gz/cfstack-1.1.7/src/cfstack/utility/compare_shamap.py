import boto3
import hashlib
import json

def compare_shamap(prod_s3,prod_calc):
    # Find keys with different values
    diff_stacks = {"Stacks":{}}
    todelete_stacks = {"Stacks":{}}
    
    for region in prod_calc["Stacks"]:
        diff_stacks["Stacks"][region] = {}
        if region in prod_s3["Stacks"]:            
            for stack in prod_calc["Stacks"][region]:
                difference = False
                if stack in prod_s3["Stacks"][region]:
                    if prod_calc["Stacks"][region][stack]["hash"] != prod_s3["Stacks"][region][stack]["hash"]:
                        difference = True
                else:
                    difference = True
                if difference:
                    diff_stacks["Stacks"][region][stack] = prod_calc["Stacks"][region][stack]
        else:
            diff_stacks["Stacks"][region] = prod_calc["Stacks"][region]    
    
    for region in prod_s3["Stacks"]:
        todelete_stacks["Stacks"][region] = {}
        if region in prod_calc["Stacks"]:            
            for stack in prod_s3["Stacks"][region]:
                if not (stack in prod_calc["Stacks"][region]):
                    todelete_stacks["Stacks"][region][stack] = prod_s3["Stacks"][region][stack]
        else:
            todelete_stacks["Stacks"][region] = prod_s3["Stacks"][region]    
    
    
    return diff_stacks,todelete_stacks 