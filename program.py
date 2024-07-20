from config import client_id, client_secret, tts_key, video_generator_key, openai_key
from redditscraper import RedditScraper
# from audiogenerator import TtsGenerator
from googleinterface import GglInterface
from videogenerator import VideoGenerator
from openai_client import GptInterface
import vidprocessor
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
    
    ggl_interface = GglInterface()
    
    if tts_input.lower() == "y":
        # tts = TtsGenerator(tts_key)
        # tts.generate_tts(title, TITLE_TTS_FILENAME, is_male)
        # tts.generate_tts(body, STORY_TTS_FILENAME, is_male)
        ggl_interface.generate_tts(title, TITLE_TTS_FILENAME, is_male)
        ggl_interface.generate_tts(body, STORY_TTS_FILENAME, is_male)


    # Get the length of the title and story in seconds
    title_length = vidprocessor.get_audio_length(TITLE_TTS_FILENAME) / 1000
    story_length = vidprocessor.get_audio_length(STORY_TTS_FILENAME) / 1000
    print(f'Length of the title is: {title_length}')
    print(f'Length of the story is: {story_length}')

    if input(f"Is one vid the length of {title_length + story_length} good? y/n ").lower() == "y":
        tts_body_files = [STORY_TTS_FILENAME]
    else:
        desired_vid_length = float(input("How long should each video be? (Enter a number in seconds) "))
        if story_length + title_length > desired_vid_length:
            needed_story_duration = desired_vid_length - title_length
            print(f'Our needed story length is: {needed_story_duration}')
            vidprocessor.split_audio(STORY_TTS_FILENAME, needed_story_duration * 1000)
            tts_body_files = vidprocessor.get_files_in_dir("audiosegments/")
    
    # upload necessary files to google drive

    gameplay_filepath = input("Enter the local filepath which points to the desired gameplay video: ")

    video_link = ggl_interface.upload_file(gameplay_filepath, "video/mp4")
    title_audio_link = ggl_interface.upload_file(TITLE_TTS_FILENAME, "audio/mpeg")

    print("File uploads complete!")

    if input("Do you want to generate a test video? y/n ") == "y":
        if len(tts_body_files) == 1:
            vidprocessor.generate_test_vid(False, tts_body_files, ggl_interface, title_audio_link, video_link, title_length)
        else:
            vidprocessor.generate_test_vid(True, tts_body_files, ggl_interface, title_audio_link, video_link, title_length)
    else:
        if(len(tts_body_files)) == 1:
            vidprocessor.generate_video(False, tts_body_files, ggl_interface, title_audio_link, video_link, title_length)
        else:
            vidprocessor.generate_video(True, tts_body_files, ggl_interface, title_audio_link, video_link, title_length)
    
    # clear out audiosegments folder
    vidprocessor.delete_all_files_in_directory("audiosegments/")

    
if __name__ == '__main__':
    main()