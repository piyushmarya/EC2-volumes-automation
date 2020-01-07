from aws_connector import AwsConnector
import botocore

class AwsOperations:
    def __init__(self):
        obj = AwsConnector()
        self.client_obj = obj.client_obj()

    def list_volumes(self):
        pass

    def attach_volume(self, vol_id, dev_id):
        pass

    def delete_volume(self, vol_id):
        try:
            response = self.client_obj.delete_volume(VolumeId=vol_id)
        except Exception as e:
            if "VolumeInUse" in str(e):
                condition = input("Continue Anyway (Y/N)")
            if condition is "Y":
                self.detach_volume(vol_id)
                resopnse = self.client_obj.delete_volume(VolumeId=vol_id)


    def detach_volume(self, vol_id):
        try:
            response = self.client_obj.detach_volume(
                VolumeId=vol_id
            )
        except botocore.exceptions.ClientError as e:
            print(e)
            if "root volume" in str(e):
                 print("Turn off instance")


    def create_volume(self, vol_id):
        pass

obj = AwsOperations()
#obj.delete_volume("vol-09288f26e1df7121e")
obj.detach_volume("vol-0e369ae1a2cd56518")