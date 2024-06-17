from config import client_id, client_secret, tts_key, video_generator_key
from redditscraper import RedditScraper
from audiogenerator import TtsGenerator
from drivepilot import GglDrivePilot
from videogenerator import VideoGenerator, save_video_to_file
import time
import requests
import sys

if __name__ == '__main__':
    # Initialize Reddit scraper to get posts
    reddit = RedditScraper(client_id, client_secret, 'Content_Filter_1/0.1 by anant_d_gr8')
    # Get posts and save them to dict
    library = dict()
    library = reddit.get_hot("pettyrevenge", 1)

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

        audio_link = drive.upload_file("elements/tts.mp3", "audio/mpeg")
        video_link = drive.upload_file("elements/minecraft_gameplay.mp4", "video/mp4")

        # print sharable elements link
        print(f'Sharable audio link: {audio_link}')
        print(f'Sharable video link: {video_link}')

        # start video generation process
        print("Now generating video...")
        v_generator = VideoGenerator(video_generator_key)
        project_id = v_generator.generate_video(audio_link, video_link)
        
        print("Checking to see if video generation is completed")
        if project_id != None:
            # we have a valid project id
            # give rendering some time
            time.sleep(40)
            # continue waiting and checking if vid is finished rendering
            vid_url = v_generator.retrieve_response(project_id)
            while(vid_url == None):
                print("vid url not generated yet. waiting 30 seconds and trying again")
                time.sleep(30)
                vid_url = v_generator.retrieve_response(project_id)
            print("Video is done generating!")
            print(f"Video url: {vid_url}")
        else:
            # no valid project id returned, exit the program
            sys.exit("No project id returned. Terminating program")
        
        # download the video
        save_video_to_file("elements/generated_video.mp4", vid_url)
