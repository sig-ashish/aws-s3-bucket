from boto3 import client,resource
from botocore.exceptions import ClientError
import os.path
import boto3
from main import db
from main.models import User
from main.secrets import access_key, secret_key

client = boto3.client('s3', aws_access_key_id =access_key, aws_secret_access_key = secret_key)


resource = boto3.resource('s3', aws_access_key_id =access_key, aws_secret_access_key = secret_key)



def get_bucket_list():
    try:
        return client.list_buckets()
    except ClientError as err:
        return err


def get_bucket_details(bucket_name):
    try:
        response = client.list_objects(Bucket=bucket_name)
        folders_list = set()
        if "Contents" in  response:
            for obj in response['Contents']:
                folders_list.add(obj['Key'].split('/',1)[0]+"/")
        bucket_name = response['Name']
        return folders_list, bucket_name 
    except ClientError as err:
        return err



def get_folder_details(bucket_name,folder_name):
    try:

        files_list = ['']
        response = client.list_objects_v2(Bucket=bucket_name, Prefix = folder_name)
        folder_list = [f["Key"]for f in response["Contents"]]
        for path in folder_list:
            files_list.append(os.path.basename(path))
        return response , files_list
    except ClientError as err:
        return err



def upload_file(file_name,bucket,key, args=None):
    try:
        return client.upload_fileobj(file_name,bucket,key, ExtraArgs=args) 
    except  ClientError as err:
        return err

def delete_file(bucket,key):

    try:
        return client.delete_object(Bucket=bucket, Key=key)
    except  ClientError as err:
        return err

def rename_file(bucket_name,folder_name,new_name,old_name):
    try:
        copy_source = {
            "Bucket": bucket_name,
            "Key" : old_name
        }
        otherkey = new_name
        print(old_name)
        resource.meta.client.copy(copy_source,bucket_name,otherkey)
        response =  delete_file(bucket_name,old_name)
        return  response
    except ClientError as err:
        return err

def copy_to_bucket(source_bucket,source_key,otherbucket,otherkey = None):
    try:
        if otherkey == None:
            otherkey = source_key
            copy_source = {
                "Bucket": source_bucket,
                "Key" : source_key
            }
            response = resource.meta.client.copy(copy_source,otherbucket,otherkey)
        else: 
            copy_source = {
                    "Bucket": source_bucket,
                    "Key" : source_key
                }
            response = resource.meta.client.copy(copy_source,otherbucket,otherkey)
        return response
    except ClientError as err:
        return err


def create_folder(bucket_name,dir_name):
        try:
           return client.put_object(Bucket=bucket_name, Body='', Key=dir_name)
        except ClientError as err:
            return err


def delete_folder(bucket_name, dir_name): 
      try:
          return resource.Bucket(bucket_name).objects.filter(Prefix=dir_name).delete()
      except ClientError as err:
            return err

