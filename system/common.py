import os
import uuid
import boto3
from system.settings import (
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    S3_BUCKET_NAME,
    S3_URL
)


def s3_upload(origin, path):

    path = 'sjahn/images'
    final_path = '{0}/{1}'.format(path, origin.name)
    # s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    # res = s3.upload_file(origin, S3_BUCKET_NAME, final_path)
    # print(res)


def s3_upload_from_obj(obj, path):
    try:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        res = s3.upload_fileobj(obj, S3_BUCKET_NAME, path)
        return {
            'path': path,
            'url': '{0}/{1}'.format(S3_URL, path)
        }
    except Exception as e:
        return False


def s3_delete(path):
    try:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        s3.delete_object(Bucket=S3_BUCKET_NAME, Key=path)
    except Exception as e:
        return False
    
    return True


def make_filename(filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename