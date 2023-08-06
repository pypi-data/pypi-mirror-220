import boto3
import hashlib
def read_file_s3(client,filedetails):
    file_missing = 0
    try:
        response = client.head_object(
            Bucket=filedetails["BucketName"],
            Key=filedetails["Key"]
        )
    except Exception as e:
        print("File not found - "+filedetails["Key"])
        file_missing = 1
    finally:
        if file_missing:
            client.get_object( Bucket=filedetails["BucketName"],Key=filedetails["Key"])
            return "File Readed"
        return "File Not Readed"