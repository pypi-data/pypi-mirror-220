import boto3
import hashlib
def upload_file_s3(client,filedetails,update=False):
    file_missing = 0
    try:
        response = client.head_object(
            Bucket=filedetails["BucketName"],
            Key=filedetails["Key"]
        )
    except Exception as e:
        file_missing = 1
    finally:
        upload = 0
        if update:
            upload = 1
        else:
            if file_missing:
                upload = 1
        if upload:
            try:
                client.upload_file(filedetails["FilePath"], filedetails["BucketName"],filedetails["Key"])
                return "File Uploaded"
            except Exception as e:
                print(e)
                return "File Not Uploaded"