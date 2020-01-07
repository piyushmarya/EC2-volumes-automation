import cmd
from cloud.aws_operations import AwsOperations
from localdb.credential_handler import CredentialHandler


class shell_aws(cmd.Cmd):

    def do_attach_volume(self, id):
        print("Hello")

    def do_detach_volume(self,id):
        print("detach_volume")
    
    def do_list_instances(self):
        print("list_instances")


if __name__ == '__main__':
    shell_aws().cmdloop()

    
