from config import video_generator_key
from pydub import AudioSegment
from pathlib import Path
import videogenerator
import vidprocessor
import requests
import shutil
import time
import sys
import os

def save_video_to_file(filename, vid_url):
    response = requests.get(vid_url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Video downloaded and savaed successfully to {filename}")
    else:
        print(f"Failed to download video. Status code: {response.status_code}")


def split_audio(input_file, segment_duration):
    audio = AudioSegment.from_mp3(input_file)
    audio_duration = get_audio_length(input_file)  # Duration in milliseconds
    
    segments = audio_duration // segment_duration
    last_segment_duration = audio_duration % segment_duration

    for i in range(int(segments)):
        start_time = i * segment_duration
        end_time = start_time + segment_duration
        segment = audio[start_time:end_time]
        segment.export(f"audiosegments/output_{int(i+1):03d}.mp3", format="mp3")

    if last_segment_duration > 0:
        start_time = segments * segment_duration
        end_time = start_time + last_segment_duration
        segment = audio[start_time:end_time]
        segment.export(f"audiosegments/output_{int(segments+1):03d}.mp3", format="mp3")


def get_audio_length(input_file):
    audio = AudioSegment.from_mp3(input_file)
    return len(audio)


def get_files_in_dir(directory_name):
    # sort the files in order of name and returns the list of files
    directory_path = Path('audiosegments/')
    files = list(directory_path.glob('output_*'))
    files.sort(key=lambda x: int(x.stem.split('_')[1]))
    
    return files

def delete_all_files_in_directory(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return

    # Check if the path is a directory
    if not os.path.isdir(directory_path):
        print(f"The path {directory_path} is not a directory.")
        return

    # Loop through all files and subdirectories in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the subdirectory and its contents
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

    print(f"All files and subdirectories in the directory {directory_path} have been deleted.")


def generate_video(is_segmented, tts_body_files, ggl_interface, title_audio_link, video_link, title_length):
    v_generator = videogenerator.VideoGenerator(video_generator_key)
    # start video generation process
    print("Now generating video...")
    # initialize counter to keep track of where each segment needs to start
    curr_vid_start_point = 0
    part = 1

    to_upload = input("Would you like the generated segment(s) to be uploaded to youtube? y/n ")

    for tts_body_file in tts_body_files:
        tts_body_file = str(tts_body_file)
        # upload the segment of tts body needed for this video
        body_audio_link = ggl_interface.upload_file(tts_body_file, "audio/mpeg")
        print(f'Current body piece video being generated: {body_audio_link}')

        if is_segmented:
            project_id = v_generator.generate_segmented_video(False, title_audio_link, body_audio_link, video_link, curr_vid_start_point, title_length, f"Part {part}")
        else:
            project_id = v_generator.generate_video(False, title_audio_link, body_audio_link, video_link, curr_vid_start_point, title_length)
        
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
        vidprocessor.save_video_to_file(f"generated/generated_video{int(part):03d}.mp4", vid_url)

        # upload the video to youtube if specified
        if to_upload.lower() == "y":
            youtube_response = ggl_interface.upload_video(f"generated/generated_video{int(part):03d}.mp4", f"Part {part}! Like and Subscribe for more #Shorts", "AITAH?", ["Shorts", "reddit", "AI", "drama", "AITAH"], "22", "public")
            print(f"Video ID: {youtube_response.get('id')}")

        # adjust counter variables for next loop through
        curr_vid_start_point += (get_audio_length(tts_body_file) / 1000)
        part += 1


def generate_test_vid(is_segmented, tts_body_files, ggl_interface, title_audio_link, video_link, title_length):
    v_generator = videogenerator.VideoGenerator(video_generator_key)
    body_file = str(tts_body_files[0])
    body_file_link = ggl_interface.upload_file(body_file, "audio/mpeg")
    print(f'Test audio piece being generated: {body_file_link}')

    if is_segmented:    
        project_id = v_generator.generate_segmented_video(True, title_audio_link, body_file_link, video_link, 0, title_length, "Part 0")
    else:
        project_id = v_generator.generate_video(True, title_audio_link, body_file_link, video_link, 0, title_length)
    
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
    vidprocessor.save_video_to_file("generated/generated_test_video.mp4", vid_url)

    if input("Would you like to generate a full video now? y/n ") == "y":
        generate_video(is_segmented, tts_body_files, ggl_interface, title_audio_link, video_link, title_length)