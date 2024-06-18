import requests
import json
import time
import sys

class VideoGenerator:

    def __init__(self, secret_key) -> None:
        self.x_api_key = secret_key


    def generate_video(self, audio_link, video_link):
        api_url = "https://api.json2video.com/v2/movies"
        headers = {
            "x-api-key": self.x_api_key,
            "Content-Type": "application/json"
        }

        json_payload = {
            "resolution": "custom",
            "height": 1280,
            "width": 720,
            "quality": "high",
            "scenes": [
                {
                    "comment": "Scene 1",
                    "elements": [
                        {
                            "type": "audio",
                            "src": audio_link,
                            "duration": 5
                        },
                        {
                            "type": "video",
                            "src": video_link,
                            "duration": -2,
                            "volume": 0
                        },
                        {
                            "type": "subtitles",
                            "language": "en",
                            "settings": {
                                "font-family": "Luckiest Guy",
                                "max-words-per-line": 1,
                                "outline-width": 7,
                                "font-size": 70,
                                "position": "center-center"
                            }
                        }
                    ]
                }
            ]
        }
        
        print("Making the call to JSON2VIDEO...")
        response = requests.post(api_url, headers=headers, data=json.dumps(json_payload))
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success"):
                project_id = response_data.get("project")
                print("Post method was a success!")
                print(f"Project ID: {project_id}")
                return project_id
            else:
                print("API call wasn't successful")
                return None
        else:
            print(f"Failed to get a valid response. Status code: {response.status_code}")
            return None


    def retrieve_response(self, project_id):
        url = f"https://api.json2video.com/v2/movies?project={project_id}"
        headers = {
            "x-api-key": self.x_api_key
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            if response_data["movie"].get("status") == "done":
                return response_data["movie"].get("url")
            elif response_data["movie"].get("status") == "error":
                print("Something went wrong!")
                sys.exit("Video status: error")                
        else:
            print(f"Failed to get a valid response. Status code: {response.status_code}")
            return None
    

def save_video_to_file(filename, vid_url):
    response = requests.get(vid_url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Video downloaded and savaed successfully to {filename}")
    else:
        print(f"Failed to download video. Status code: {response.status_code}")