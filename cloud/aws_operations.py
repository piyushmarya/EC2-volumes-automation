import botocore
from cloud.aws_connector import AwsConnector


class AwsOperations:
    def __init__(self):
        """
        """
        obj = AwsConnector()
        self.client_obj = obj.client_obj()
        self.created_volumes = []

    def take_input(self, message):
        inp = ""
        while inp == "":
            inp = input(message)
        return inp

    def describe_volume(self, vol_id):
        """
        """
        try:
            response = self.client_obj.describe_volumes(
                 VolumeIds=[vol_id, ]
            )
            return response

        except botocore.exceptions.ClientError as e:
            print(e)

    def list_all_volumes(self):
        """
        """
        region = self.take_input("Enter region from which you want to list volumes: ")
        try:
            response = self.client_obj.describe_volumes(
                Filters=[
                    {
                         'Name': 'availability-zone',
                         'Values': [region, ]
                    }
                ]
            )

            for r in response['Volumes']:
                if r['Attachments']:
                    print("\nVolumeId: "+r['VolumeId'])
                    print("Size: "+str(r['Size']))
                    print("Attached To instance '"+r['Attachments'][0]['InstanceId']+"' as '"+r['Attachments'][0]['Device']
                          + "'")
                else:
                    print("\nVolumeId: " + r['VolumeId'])
                    print("Size: " + str(r['Size']))
                    print("Volume is not attached to any instance.")

        except botocore.exceptions.ClientError as e:
            print(e)

    def attach_volume(self):
        """
        """
        vol_id = self.take_input("Enter id of the volume: ")
        inst_id = self.take_input("Enter id of instance to which the volume is to be attached: ")
        dev_name = self.take_input("Enter the device name as which you want to attach the volume: ")

        try:
            response = self.client_obj.attach_volume(
                VolumeId=vol_id,
                InstanceId=inst_id,
                Device=dev_name
                )
            print("\nAttaching...")
            waiter = self.client_obj.get_waiter('volume_in_use')
            waiter.wait(VolumeIds=[vol_id, ])

        except botocore.exceptions.ClientError as e:
            print(e)
        print("Attached\n")

    def delete_volume(self, vol_id=None):
        """
        """
        condition = "N"
        if vol_id is None:
            vol_id = self.take_input("Enter the id of the volume to be deleted: ")

        try:
            response = self.client_obj.delete_volume(VolumeId=vol_id)
            print("\nDeleting...")
            waiter = self.client_obj.get_waiter('volume_deleted')
            waiter.wait(VolumeIds=[vol_id])

        except botocore.exceptions.ClientError as e:
            print(e)
            if "VolumeInUse" in str(e):
                condition = input("Continue Anyway (Y/N)")
                if condition is "Y":
                    if self.detach_volume(vol_id):
                        self.delete_volume(vol_id)

        if vol_id in self.created_volumes:
            print("Deleted\n")
            self.created_volumes.remove(vol_id)

    def detach_volume(self, vol_id=None):
        """
        """
        if vol_id is None:
            vol_id = self.take_input("Enter the id of the volume to be detached: ")

        try:
            response = self.client_obj.detach_volume(
                VolumeId=vol_id
            )
            print("\nDetaching...")
            waiter = self.client_obj.get_waiter('volume_available')
            waiter.wait(VolumeIds=[vol_id])

        except botocore.exceptions.ClientError as e:
            print(e)
            if "root volume" in str(e):
                print("Turn off instance")
                return 0
        print("Detached\n")
        return 1

    def create_volume(self):
        """
        """
        size = int(self.take_input("Enter size(gb) of the volume to be created: "))
        type_vol = self.take_input("Enter type of the volume(gp2,iop,standard,etc)")
        region = self.take_input("Enter the region in which u want to create volume(example:us-east-2c): ")

        try:
            response = self.client_obj.create_volume(
                AvailabilityZone=region,
                Size=size,
                VolumeType=type_vol,
            )
            print("\nCreating...")
            waiter = self.client_obj.get_waiter('volume_available')
            waiter.wait(VolumeIds=[response['VolumeId'], ])

        except botocore.exceptions.ClientError as e:
            print(e)

        else:
            self.created_volumes.append(response['VolumeId'])
            print("Created/n")
    def print_new_volumes(self):
        """
        """
        if not len(self.created_volumes):
            print("No new volumes")
        for i in self.created_volumes:
            vol_info = self.describe_volume(i)
            print(i + " created on "+str(vol_info["Volumes"][0]['CreateTime']))
