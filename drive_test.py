from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

try:
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() 
    drive = GoogleDrive(gauth)

    folder = drive.CreateFile({'title': 'text.txt', 'parents': [{'id': '1y5Zs-VIlg_U935EHQDxLHdWXfHa5gCG3'}]})
    folder.Upload()
except Exception as e:
    print(f"An error occurred: {e}")