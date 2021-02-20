#!/usr/bin/python
import sys, os, re
from pytube import YouTube

#function to remove files from folder
def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))

#Delete audio and video files from previous downloads
purge(".", "audio")
purge(".", "video")

yt_link = sys.argv[1]
yt = YouTube(yt_link)
audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
audio_file = 'audio.'+audio_stream.default_filename.split('.')[-1]
video_stream = yt.streams.filter(file_extension='webm').order_by('resolution').desc().first()
video_file = 'video.'+video_stream.default_filename.split('.')[-1]
video_title = video_stream.title.replace(" ", "-")

#Print video title
print(video_title)

print("Downloading audio...")
audio_download = audio_stream.download(filename='audio')

print("Downloading video...")
video_download = video_stream.download(filename='video')

print("Merging audio e vídeo...")
os.system("ffmpeg -i "+audio_file+" -i "+video_file+" -c copy "+video_title+".mp4")

#Delete audio and video files
purge(".", "audio")
purge(".", "video")

print("Finished")