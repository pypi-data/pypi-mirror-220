import boto3
import hashlib
def upload_template_s3(inputs):
    s3 = boto3.client('s3')
    should_upload = 0
    try:
        response = s3.head_object(
            Bucket=inputs["BucketName"],
            Key=inputs["TemplateName"]
        )
        with open(inputs["TemplatePath"], 'rb') as file:
            checksum = hashlib.md5(file.read()).hexdigest()
        if checksum != response['ETag'].strip('"'):
            print("uploaded from local (checksum mismatched)"+inputs["TemplateName"])          
            should_upload = 1 
        else:
            print("Template pressent but not updated")
            return 1
    except:
        print("uploaded from local (file not found)"+inputs["TemplateName"])
        should_upload = 1
    finally:
        if should_upload:
            s3.upload_file(inputs["TemplatePath"], inputs["BucketName"],inputs["TemplateName"])
            return 0
        return 1