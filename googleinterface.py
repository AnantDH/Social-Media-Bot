from __future__ import print_function
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.cloud import texttospeech
import os

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/youtube.upload']
# service key to authenticate for google tts service
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "json_secrets/redditproject-426518-d62ef007d17f.json"

class GglInterface:
    def __init__(self) -> None:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('json_secrets/token.json'):
            creds = Credentials.from_authorized_user_file('json_secrets/token.json', SCOPES)
        
        # If there are no valid credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'json_secrets/credentials.json', SCOPES)
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run.
            with open('json_secrets/token.json', 'w') as token:
                token.write(creds.to_json())

        self.drive_service = build('drive', 'v3', credentials=creds)
        self.youtube_service = build('youtube', 'v3', credentials=creds)
        self.tts_service = texttospeech.TextToSpeechClient()
    
    
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
    

    def generate_tts(self, text_input, output_filename, is_male):
        if is_male == "True":
            # middle aged man voice
            voice_name = "en-US-Neural2-J"
            # young man annoying voice
            # voice_name = "en-US-Neural2-A"
            # deeper man voice
            # voice_name = "en-US-Neural2-D"
        else:
            # middle aged female voice
            voice_name = "en-US-Neural2-C"
            # middle aged female voice (higher pitch)
            # voice_name = "en-US-Neural2-E"
            # younger female voice (kind of annoying)
            # voice_name = "en-US-Neural2-F"
            # younger female voice
            # voice_name = "en-US-Neural2-G"
            # higher pitched female voice
            # voice_name = "en-US-Neural2-H"




        synthesis_input = texttospeech.SynthesisInput(text=text_input)

        # Build the voice request, select the language code ("en-US") and the ssml
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name=voice_name
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.11
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.tts_service.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(output_filename, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f'Audio content written to file {output_filename}')
