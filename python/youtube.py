from spotify import get_playlist_tracks
import urllib.request
from pytube import YouTube
import re
import sys


# Define playlist URL
Playlist_url = sys.argv[1]

# Create an empty list to store playlist tracks
song_name_lists = []
get_playlist_tracks(Playlist_url, song_name_lists)

song_name_lists = [song.replace(" ", "+") for song in song_name_lists]
#Define youtube URL lists
youtube_url_lists = []

#Uploading URLS to youtube_url_lists by searching song names
for song_name in song_name_lists:
    song_link = r"https://www.youtube.com/results?search_query=" + song_name
    song_link = song_link.encode('ascii', 'ignore').decode('ascii')
    html  = urllib.request.urlopen(song_link)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = r"https://www.youtube.com/watch?v=" + video_ids[0]
    youtube_url_lists.append(url)

def download_audio(video_url):
    video = YouTube(video_url)
    audio = video.streams.filter(only_audio = True).first()
    AUDIO_SAVE_DIRECTORY = sys.argv[2]
    try:
        audio.download(AUDIO_SAVE_DIRECTORY)
    except:
        print("Failed to download audio")


for idx,url in enumerate(youtube_url_lists):
        print(f"Downloading {idx+1}/{len(youtube_url_lists)}: {song_name_lists[idx]}")
        download_audio(url)
