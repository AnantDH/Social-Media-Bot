from __future__ import print_function
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/youtube.upload']

class GglInterface:
    def __init__(self) -> None:
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

        self.drive_service = build('drive', 'v3', credentials=creds)
        self.youtube_service = build('youtube', 'v3', credentials=creds)
    
    
    def upload_file(self, filename, mimetype):
        # Call the Drive v3 API to upload a file.
        file_metadata = {'name': filename}
        media = MediaFileUpload(filename, mimetype=mimetype)
        file = self.drive_service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
        file_id = file.get('id')
        print('File ID: %s' % file_id)
        
        # Set the file to be sharable
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        self.drive_service.permissions().create(
            fileId=file_id,
            body=permission
        ).execute()
        
        # Get the shareable link
        file = self.drive_service.files().get(fileId=file_id, fields='webViewLink').execute()
        shareable_link = file.get('webViewLink')
        return shareable_link
    

    def upload_video(self, filename, title, description, tags, category_id, privacy_status):
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status
            }
        }
        
        media = MediaFileUpload(filename, chunksize=-1, resumable=True)
        
        request = self.youtube_service.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")
        print("Upload Complete!")
        return response        
