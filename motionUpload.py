from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

class GDrive(object):
    def __init__(self):
        self.drive = None
        self.folderID = '1ZMa9itBlwza30otOLA0DYZlLrb7Cjj4o'
        if self.drive == None:
            print('[INFO] Login initiated...')
            print('[INFO] Please login')
            self.login()

    def login(self):
        g_login = GoogleAuth()
        g_login.LocalWebserverAuth()
        self.drive = GoogleDrive(g_login)

    def setPath(self, path):
        self.path = path

    def upload(self):
        with open(self.path, "r") as file:
            file_drive = self.drive.CreateFile({'title':os.path.basename(file.name), "parents": [{"kind": "drive#fileLink", "id": self.folderID}] })
            file_drive.SetContentFile(self.path)
            file_drive.Upload()
            print(self.path)
            
