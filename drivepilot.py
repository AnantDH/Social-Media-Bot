from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GglDrivePilot:
    def __init__(self) -> None:
        """Shows basic usage of the Drive v3 API.
        Uploads a file to the user's Google Drive.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # If there are no valid credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run.
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)
    
    
    def upload_file(self, filename, mimetype):
        # Call the Drive v3 API to upload a file.
        file_metadata = {'name': filename}
        media = MediaFileUpload(filename, mimetype=mimetype)
        file = self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
        file_id = file.get('id')
        print('File ID: %s' % file_id)
        
        # Set the file to be sharable
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        self.service.permissions().create(
            fileId=file_id,
            body=permission
        ).execute()
        
        # Get the shareable link
        file = self.service.files().get(fileId=file_id, fields='webViewLink').execute()
        shareable_link = file.get('webViewLink')
        return shareable_link
