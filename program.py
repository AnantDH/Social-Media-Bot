from config import client_id, client_secret, tts_key, video_generator_key
from redditscraper import RedditScraper
from audiogenerator import TtsGenerator
from drivepilot import GglDrivePilot
from videogenerator import VideoGenerator
import time
import requests

if __name__ == '__main__':
    # Initialize Reddit scraper to get posts
    reddit = RedditScraper(client_id, client_secret, 'Content_Filter_1/0.1 by anant_d_gr8')
    # Get posts and save them to dict
    library = dict()
    library = reddit.get_controversial("AITAH", 1)

    # Initialize TTS generator
    tts = TtsGenerator(tts_key)

    
    # Loop through stories
    for key in library:
        body, score = library[key]
        # Generate an MP3 file with the TTS of the story
        print(key)  # Prints the title of the story to console
        
        # tts.generate_tts(key + body, True)

        # upload necessary files to google drive
        drive = GglDrivePilot()

        drive.upload_file("output.mp3", "audio/mpeg")

        # start video generation process
        # print("Now generating video...")
        # v_generator = VideoGenerator(video_generator_key)
        # project_id = v_generator.generate_video()
        # # wait for generation to start occurring
        # print("Waiting for video generation to occurr..")
        # time.sleep(60)
        # print("Checking to see if video generation is completed")
        # if project_id != None:
        #     vid_url = v_generator.retrieve_response(project_id)
        # if(vid_url != None):
        #     print("Video is done!")
        #     print(vid_url)
        # else:
        #     print("Video not done or some other error occurred...")
        
        # # download the video
        # save_to = "generated_video.mp4"
        # response = requests.get(vid_url, stream=True)
        # if response.status_code == 200:
        #     with open(save_to, 'wb') as f:
        #         for chunk in response.iter_content(chunk_size=8192):
        #             f.write(chunk)
        #     print(f"Video downloaded and savaed successfully to {save_to}")
        # else:
        #     print(f"Failed to download video. Status code: {response.status_code}")
