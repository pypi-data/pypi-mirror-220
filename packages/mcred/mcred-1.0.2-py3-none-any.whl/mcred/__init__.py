from mclass import DictClass
import json
import pathlib
import os
import pysftp
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None    # disable host key checking.


class CredManager:
    def __init__(self, host=None, port=None, username=None, password=None, remote_credentials_file_path=None):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.remote_file_path = remote_credentials_file_path
        self.local_file_path = os.path.join(pathlib.Path(__file__).parent, "credentials.json")
        

    def pull(self, force=False):
        if not os.path.exists(self.local_file_path) or force:
            with pysftp.Connection(
                host=self.host, 
                username=self.username, 
                password=self.password,
                port=self.port,
                cnopts=cnopts,
            ) as sftp:
                print(f"Downloading credentials from {self.remote_file_path} to {self.local_file_path})")
                sftp.get(remotepath=self.remote_file_path, localpath=self.local_file_path)

    def get(self):
        if os.path.exists(self.local_file_path):
            credentials_dict = json.load(open(self.local_file_path, "r"))
            Credentials = DictClass(credentials_dict)
        else:
            Credentials = DictClass({})
            
        return Credentials