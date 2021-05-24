import os
import boto3
from AWSUtils.config import ACCESS_KEY, SECRET_KEY


class Aws:
    def __init__(self, resource):
        """

        :param resource:
        """
        self.access_key = os.environ.get('AWS_ACCESS_KEY_ID', ACCESS_KEY)
        self.secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY', SECRET_KEY)
        self.resource = resource

    def get_resource_object(self):
        """

        :return:
        """
        aws_object = boto3.resource(self.resource,
                                    aws_access_key_id=self.access_key,
                                    aws_secret_access_key=self.secret_key)
        return aws_object

    def get_client_object(self):
        aws_client_object = boto3.client(self.resource,
                                         aws_access_key_id=self.access_key,
                                         aws_secret_access_key=self.secret_key,
                                         region_name='us-west-2')
        return aws_client_object


class S3:
    def __init__(self):
        self.aws_object = Aws(resource='s3')
        self.s3 = self.aws_object.get_resource_object()
        self.s3_client = self.aws_object.get_client_object()

    def get_all_buckets(self):
        """

        :return:
        """
        bucket_info = []
        try:
            for bucket in self.s3.buckets.all():
                bucket_info.append(bucket)
        except Exception as err_msg:
            print('Error: {}'.format(err_msg))

        return bucket_info

    def create_bucket(self, bucket_name, region):
        """

        :param bucket_name:
        :param region:
        :return:
        """
        status = False
        try:
            location = {'LocationConstraint': region}
            response = self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
            if response:
                status = True
        except Exception as err_msg:
            print('Error: {}'.format(err_msg))

        return status


class CF:
    def __init__(self):
        self.aws_object = Aws(resource='cloudformation')
        self.cf_client = self.aws_object.get_client_object()

    def stack_exists(self, stack_name=''):
        """

        :param stack_name:
        :return:
        """
        status = False
        try:
            stacks = self.cf_client.list_stacks()['StackSummaries']
            for stack in stacks:
                print(stack)
        except Exception as err_msg:
            print('Error: {}'.format(err_msg))

        return status

    def create_stack(self, template_file='', template_params=''):
        """

        :param template_file:
        :param template_params:
        :return:
        """
        import pdb
        pdb.set_trace()
        status = False
        template_params = {
            "DBName": "abhiabhi",
            "DBUser": "abhi",
            "DBPassword": "abhi123",
            "DBRootPassword": "abhi123",
            "Region": 'us-east-1',
            "StackName": 'abhi-db-cf-new',
            "InstanceType": 't2.micro',
            "KeyName": 'abhi-ssh',
        }
        try:
            stacks = self.cf_client.create_stack(**template_params)
            for stack in stacks:
                print(stack)
        except Exception as err_msg:
            print('Error: {}'.format(err_msg))

        return status

