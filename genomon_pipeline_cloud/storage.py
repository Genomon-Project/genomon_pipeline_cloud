#! /usr/bin/env python

import sys, re
from subprocess32 import Popen, PIPE
import boto3

class Storage(object):

    def __init__(self, region = None, zone = None):

        """
        if region is None and zone is None:
            print >> sys.stderr, "region or zone should not be None."
            sys.exit(1)
        """
        self.provider = None
        self.region = region
        self.zone = zone


    def upload(self, local_file_path, storage_path, create_bucket = False):
        
        if storage_path.startswith("s3://"):
            self.__upload_to_aws(local_file_path, storage_path, create_bucket)
        elif storage_path.startswith("gs://"):
            self.__upload_to_gcs(local_file_path, storage_path, create_bucket)
        else:
            raise ValueError, "Storage path should starts with 's3://' or 'gs://'."

        
    def __get_bucket_name_from_storage_path(self, storage_path):

        if storage_path.startswith("s3://"):
            return re.sub(r'^s3://', '', storage_path).split('/')[0]
        elif storage_path.startswith("gs://"):
            return re.sub(r'^gs://', '', storage_path).split('/')[0]
        else:
            raise ValueError, "Storage path should starts with 's3://' or 'gs://'."



    def __upload_to_aws(self, local_file_path, storage_path, create_bucket = False):
        
        # Extract AWS S3 bucket name of the storage_path argument
        target_bucket_name = self.__get_bucket_name_from_storage_path(storage_path)

        if not check_bucket_exist_aws(target_bucket_name):
            if create_bucket:
                s3 = boto3.client("s3")
                s3.create_bucket(Bucket = target_bucket_name)
            else:
                print >> sys.stderr, "No bucket: " + target_bucket_name
                sys.exit(1)

        # Upload to the S3
        storage_file_name = '/'.join(re.sub(r'^s3://', '', storage_path).split('/')[1:])
        s3.upload_file(local_file_path, target_bucket_name, storage_file_name) 


    def __upload_to_gcs(self, local_file_path, storage_path, create_bucket = False):

        # Extract Google Cloud Storage bucket name if the storage_path argument
        target_bucket_name = self.__get_bucket_name_from_storage_path(storage_path)

        if not __check_bucket_exist_gcs(target_bucket_name):

            if create_bucket:
                proc = Popen(["gsutil", "mb", 'gs://' + target_bucket_name], stdout = PIPE, stderr = PIPE)
                out, err = proc.communicate()
                if proc.returncode == 1:
                    if "ServiceException" in err:
                        print >> sys.stderr, "Bucket " + target_bucket_name + " already exists."
                        sys.exit(1)
                    else:
                        print >> sys.stderr, "An Error happend while creating Buckt " + target_bucket_name + "."
                        sys.exit(1)
            else:
                print >> sys.stderr, "No bucket: " + target_bucket_name
                sys.exit(1)

        # Upload to the Google Cloud Storage
        proc = Popen(["gsutil", "cp", local_file_path, storage_path], stdout = PIPE, stderr = PIPE)
        out = proc.communicate()



    def __check_bucket_exist_aws(self, bucket_name):

        import boto3

        s3 = boto3.client("s3")
        response = s3.list_buckets()
        available_bucket_names = [bucket["Name"] for bucket in response["Buckets"]]

        if bucket_name in available_bucket_names:
            return True
        else:
            return False


    def __check_bucket_exist_gcs(self, bucket_name):

        from subprocess32 import Popen, PIPE

        proc = Popen(["gsutil", "ls"], stdout = PIPE, stderr = PIPE)
        available_bucket_names = [re.sub(r'^gs://', '', x).rstrip('/') for x in proc.communicate()[0].split('\n')]

        if bucket_name in available_bucket_names:
            return True
        else:
            return False



    def __create_bucket_gcs(self, bucket_name):

        proc = Popen(["gsutil", "mb", 'gs://' + bucket_name], stdout = PIPE, stderr = PIPE)
        out, err = proc.communicate()
        if proc.returncode == 1:
            if "ServiceException" in err:
                print >> sys.stderr, "Bucket " + bucket_name + " already exists."
                sys.exit(1)
            else:
                print >> sys.stderr, "An Error happend while creating Buckt " + bucket_name + "."
                sys.exit(1)


if __name__ == "__main__":

    storage = Storage()
    storage.upload("test.txt", "gs://friend1_upload_test/test.txt", True)  

