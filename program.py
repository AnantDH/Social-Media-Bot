from config import client_id, client_secret, tts_key, video_generator_key, openai_key
from redditscraper import RedditScraper
from audiogenerator import TtsGenerator
from googleinterface import GglInterface
from videogenerator import VideoGenerator
from openai_client import GptInterface
from vidprocessor import save_video_to_file, split_audio, get_audio_length, get_files_in_dir
import time
import sys

TITLE_TTS_FILENAME = "elements/title_tts.mp3"
STORY_TTS_FILENAME = "elements/story_tts.mp3"

def main():
    print("Welcome to Content Machine 1.0.5!")

    # ask if user wants to link a post or find one through praw
    user_input = input("Enter a URL to a post or a subreddit from which you'd like to get a post ")
    
    reddit = RedditScraper(client_id, client_secret, 'Content_Filter_1/0.1 by anant_d_gr8')
    # is a url
    if "https://" in user_input:
        title, body = reddit.get_url(user_input)
    # is a subreddit they want to search
    else:
        n = input("Which hot post would you like from the top? ")
        title, body = reddit.get_nth_hot(input, int(n))

    print(f"Title of story to be generated: {title}")

    print("Querying gpt to see whether story writer is a male or female")
    gpt = GptInterface(openai_key)
    is_male = gpt.get_is_male(body)
    print(f"Is the writer a male: {is_male}")
    is_male = input("What should it be? True/False ")
    print(f"Is the writer a male is now: {is_male}")

    tts_input = input("Would you like to generate tts for this story or use existing ones generated? y/n ")
    
    
    if tts_input.lower() == "y":
        tts = TtsGenerator(tts_key)
        tts.generate_tts(title, TITLE_TTS_FILENAME, is_male)
        tts.generate_tts(body, STORY_TTS_FILENAME, is_male)

    # Get the length of the title and story in seconds
    title_length = get_audio_length(TITLE_TTS_FILENAME) / 1000
    story_length = get_audio_length(STORY_TTS_FILENAME) / 1000
    print(f'Length of the title is: {title_length}')
    print(f'Length of the story is: {story_length}')

    if input(f"Is one vid the length of {title_length + story_length} good? y/n ").lower() == "y":
        tts_body_files = [STORY_TTS_FILENAME]
    else:
        desired_vid_length = float(input("How long should each video be? (Enter a number in seconds) "))
        if story_length + title_length > desired_vid_length:
            needed_story_duration = desired_vid_length - title_length
            print(f'Our needed story length is: {needed_story_duration}')
            split_audio(STORY_TTS_FILENAME, needed_story_duration * 1000)
            tts_body_files = get_files_in_dir("audiosegments/")
    
    # upload necessary files to google drive
    ggl_interface = GglInterface()

    gameplay_filepath = input("Enter the local filepath which points to the desired gameplay video: ")

    video_link = ggl_interface.upload_file(gameplay_filepath, "video/mp4")
    title_audio_link = ggl_interface.upload_file(TITLE_TTS_FILENAME, "audio/mpeg")

    print("File uploads complete!")

    if input("Do you want to generate a test video? y/n ") == "y":
        generate_test_vid(tts_body_files, ggl_interface, title_audio_link, video_link, title_length)
    else:
        generate_video(tts_body_files, ggl_interface, title_audio_link, video_link, title_length)

def generate_test_vid(tts_body_files, ggl_interface, title_audio_link, video_link, title_length):
    v_generator = VideoGenerator(video_generator_key)
    body_file = str(tts_body_files[0])
    body_file_link = ggl_interface.upload_file(body_file, "audio/mpeg")
    print(f'Test audio piece being generated: {body_file_link}')
    
    project_id = v_generator.generate_segmented_video(True, title_audio_link, body_file_link, video_link, 0, title_length, f"Part {1}")
        
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
    print("Saving test file..")
    save_video_to_file("elements/generated_video.mp4", vid_url)


def generate_video(tts_body_files, ggl_interface, title_audio_link, video_link, title_length):
    v_generator = VideoGenerator(video_generator_key)
    # start video generation process
    print("Now generating video...")
    # initialize counter to keep track of where each segment needs to start
    curr_vid_start_point = 0
    part = 1
    for tts_body_file in tts_body_files:
        tts_body_file = str(tts_body_file)
        # upload the segment of tts body needed for this video
        body_audio_link = ggl_interface.upload_file(tts_body_file, "audio/mpeg")
        print(f'Current body piece video being generated: {body_audio_link}')

        project_id = v_generator.generate_segmented_video(False, title_audio_link, body_audio_link, video_link, curr_vid_start_point, title_length, f"Part {part}")
        
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

        # upload the video to youtube
        youtube_response = ggl_interface.upload_video("elements/generated_video.mp4", f"Part {part}! Like and Subscribe for more #Shorts", "AITAH?", ["Shorts", "reddit", "AI", "drama", "AITAH"], "22", "public")
        print(f"Video ID: {youtube_response.get('id')}")

        # adjust counter variables for next loop through
        curr_vid_start_point += 59.5
        part += 1

if __name__ == '__main__':
    main()