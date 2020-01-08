import json
FILENAME = "credential//credential.json"

class CredentialHandler:
    
    def take_input(self):
        secret_key = input("Input secret key: ")
        access_key = input("Enter access key: ")
        region = input("Enter region: ")
        user_credentials = {"Secret key":secret_key,
                            "Access key":access_key,
                            "Region": region
                        }
#        print(user_credentials)
        with open(FILENAME, 'w+') as credential:
            json.dump(user_credentials, credential, indent=4)
        
    def update_credential(self, **kwargs):
        with open(FILENAME, 'r') as credential:
            data = json.load(credential)
        if kwargs["secret_key"]:
             data["Secret key"] = kwargs["secret_key"]
        if kwargs["access_key"]:
             data["Access key"] = kwargs["access_key"]
        if kwargs["region"]:
             data["Region"] = kwargs["region"]
        with open(FILENAME, 'w+') as credential:
             json.dump(data, credential, indent=4)
     
    def return_json(self):
        with open(FILENAME, 'r') as credential:
            data = json.load(credential)
        return data
