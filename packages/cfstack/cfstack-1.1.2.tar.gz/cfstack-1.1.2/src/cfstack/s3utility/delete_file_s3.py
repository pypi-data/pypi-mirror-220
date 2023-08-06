import boto3
import hashlib
def delete_file_s3(client,filedetails):
    file_missing = 0
    try:
        response = client.head_object(
            Bucket=filedetails["BucketName"],
            Key=filedetails["Key"]
        )
    except Exception as e:
        file_missing = 1
    finally:
        if not file_missing:
            try:
                client.delete_object(Bucket=filedetails["BucketName"],Key=filedetails["Key"])
                return "File Deleted"
            except Exception as e:
                print(e)
                return "File Not Deleted"