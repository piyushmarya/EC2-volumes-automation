#This file reads the credentials and return a ec2 client object
import boto3
import botocore
from credential.credential_handler import CredentialHandler


class AwsConnector:
    
    def __init__(self):
        """
        storing credetnials in a instance variable
        """
        obj = CredentialHandler()
        self.credentials = obj.return_json()
        # print(self.credentials)

    def client_obj(self):
        try:
            client = boto3.Session.client(
                boto3.session.Session(),
                service_name="ec2",
                region_name=self.credentials["Region"],
                aws_access_key_id=self.credentials["Access key"],
                aws_secret_access_key=self.credentials["Secret key"],
            )
        except botocore.Exception as e:
            print(e)

        return client
