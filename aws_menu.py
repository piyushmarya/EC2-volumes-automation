from cloud.aws_operations import AwsOperations

cloud_obj = AwsOperations()

USER_CHOICE = '''\nEnter one of the following
- 'create' to create a new volume.
- 'delete' to delete.
- 'describe all' to describe all volumes in the specified region.
- 'attach' to attach a volume to a instance.
- 'detach' to detach a volume from a instance.
- list new' to print newly created volumes.
- 'q' to exit.
Enter your choice: '''

user_choices = {
    'create': cloud_obj.create_volume,
    'delete': cloud_obj.delete_volume,
    'detach': cloud_obj.detach_volume,
    'attach': cloud_obj.attach_volume,
    'describe all': cloud_obj.list_all_volumes,
    'list new': cloud_obj.print_new_volumes
}


def menu():
    user_input = input(USER_CHOICE)
    while user_input != 'q':
        if user_input in ('create', 'delete', 'detach', 'attach', 'describe all', 'list new'):
            user_choices[user_input]()
        else:
            print('Please choose a valid command.')
        user_input = input(USER_CHOICE)
        
if __name__ == "__main__":
    menu()
