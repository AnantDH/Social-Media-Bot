from pydub import AudioSegment
import requests
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
    file_list = []
    for filename in os.listdir(directory_name):
        file_path = os.path.join(directory_name, filename)
        if os.path.isfile(file_path):
            file_list.append(file_path)
    return file_list



# Splits a given mp3 file into two segments, one which is the specified length, the other is the rest of the file
# def split_audio(input_file, segment_duration):
#     audio = AudioSegment.from_mp3(input_file)
    
#     # get the filename without the .mp3 part
#     base_filename = input_file.rsplit(".", 1)[0]

#     # get datetime to make unique output files
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

#     # specify the segments of the audio we want in the two segments
#     first_segment = audio[:segment_duration]
#     second_segment = audio[segment_duration:]

#     # save two new segment filenames
#     segment1_filename = f"{base_filename}_part1_{timestamp}.mp3"
#     segment2_filename = f"{base_filename}_part2_{timestamp}.mp3"

#     # export the segments
#     first_segment.export(segment1_filename, format="mp3")
#     second_segment.export(segment2_filename, format="mp3")

#     return segment1_filename, segment2_filename