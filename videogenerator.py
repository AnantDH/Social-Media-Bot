import requests
import json
import time
import sys

class VideoGenerator:

    def __init__(self, secret_key) -> None:
        self.x_api_key = secret_key

    def generate_segmented_video(self, is_test, title_audio_link, body_audio_link, video_link, curr_vid_start_point, title_length, part):
        if is_test:
            duration = 2
        else:
            duration = -1

        api_url = "https://api.json2video.com/v2/movies"
        headers = {
            "x-api-key": self.x_api_key,
            "Content-Type": "application/json"
        }

        json_payload = {
            "resolution": "custom",
            "height": 852,
            "width": 480,
            "quality": "high",
            "scenes": [
                {
                    "comment": "scene 1",
                    "duration": duration,
                    "elements": [
                        {
                            "type": "audio",
                            "src": title_audio_link
                        },
                        {
                            "type": "video",
                            "src": video_link,
                            "duration": -2,
                            "volume": 0,
                            "seek": curr_vid_start_point,
                            "height": 852,
                            "width": 480
                        },
                        {
                            "type": "audio",
                            "src": body_audio_link,
                            "start": title_length + 0.3
                        },
                        {
                            "type": "text",
                            "style": "007",
                            "x": 0,
                            "y": -220,
                            "text": part,
                            "settings": {
                                "text-shadow": "11px 11px black",
                                "color": "#f20202",
                                "font-size": "65px",
                                "font-family": "Luckiest Guy",
                                "font-weight": "400"
                            },
                            "duration": -2
                        },
                        {
                            "type": "subtitles",
                            "language": "en",
                            "settings": {
                                "font-family": "Luckiest Guy",
                                "max-words-per-line": 1,
                                "outline-width": 4,
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
        return self.check_vid_response(response)
    

    def generate_video(self, is_test, title_audio_link, body_audio_link, video_link, curr_vid_start_point, title_length):
        if is_test:
            duration = 2
        else:
            duration = -1

        api_url = "https://api.json2video.com/v2/movies"
        headers = {
            "x-api-key": self.x_api_key,
            "Content-Type": "application/json"
        }

        json_payload = {
            "resolution": "custom",
            "height": 852,
            "width": 480,
            "quality": "high",
            "scenes": [
                {
                    "comment": "scene 1",
                    "duration": duration,
                    "elements": [
                        {
                            "type": "audio",
                            "src": title_audio_link
                        },
                        {
                            "type": "video",
                            "src": video_link,
                            "duration": -2,
                            "volume": 0,
                            "seek": curr_vid_start_point,
                            "height": 852,
                            # "width": 480
                            "x": -460
                        },
                        {
                            "type": "audio",
                            "src": body_audio_link,
                            "start": title_length + 0.3
                        },
                        {
                            "type": "subtitles",
                            "language": "en",
                            "settings": {
                                "font-family": "Luckiest Guy",
                                "max-words-per-line": 1,
                                "outline-width": 4,
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
        return self.check_vid_response(response)
        
        
    def check_vid_response(self, response):
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