# Import necessary libraries
import requests  # Used for making HTTP requests
import json  # Used for working with JSON data

class TtsGenerator:


    def __init__(self, secret_key):  
        # Define constants for the script
        self.CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
        self.XI_API_KEY = secret_key  # Your API key for authentication
    
    
    def generate_tts(self, text, output_filename, isMale):
        if(isMale):
            VOICE_ID = "AaNV2Mbw4bC4yyB5KWqa"
        else:
            VOICE_ID = "sASxGd32xItBb17GWuFk"
        
        TEXT_TO_SPEAK = text  # Text you want to convert to speech
        OUTPUT_PATH = output_filename  # Path to save the output audio file

        # Construct the URL for the Text-to-Speech API request
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

        # Set up headers for the API request, including the API key for authentication
        headers = {
            "Accept": "application/json",
            "xi-api-key": self.XI_API_KEY
        }

        # Set up the data payload for the API request, including the text and voice settings
        data = {
            "text": TEXT_TO_SPEAK,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }

        # Make the POST request to the TTS API with headers and data, enabling streaming response
        response = requests.post(tts_url, headers=headers, json=data, stream=True)

        # Check if the request was successful
        if response.ok:
            # Open the output file in write-binary mode
            with open(OUTPUT_PATH, "wb") as f:
                # Read the response in chunks and write to the file
                for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                    f.write(chunk)
            # Inform the user of success
            print("Audio stream saved successfully.")
        else:
            # Print the error message if the request was not successful
            print(response.text)
