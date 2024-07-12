from pydub import AudioSegment
import requests
import os
from pathlib import Path

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