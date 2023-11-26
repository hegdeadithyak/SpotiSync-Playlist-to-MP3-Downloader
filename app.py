import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import urllib.request
from pytube import YouTube
import re
import sys


# Get the client_id from environment variables
client_id = "535e76588a5b4c6db491cd633213c3ec"

client_secret = "3ffeca84b6084f47aeb4f2be647b0df0"

# Create a Spotify client
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Define the playlist URL
playlist_url = 'https://open.spotify.com/playlist/37i9dQZF1DWTwbZHrJRIgD?si=42e6b58c9d18453e'

# Function to get song names and artists from a playlist
def get_playlist_tracks(playlist_url,song_list=[]):
    # Extract the playlist ID from the URL
    playlist_id = playlist_url.split('/')[-1]
    playlist_id = playlist_id.split('?')[0]
    results = sp.user_playlist_tracks('spotify', playlist_id)

    for track in results['items']:
        track_info = track['track']
        track_name = track_info['name']
        artists = [artist['name'] for artist in track_info['artists']]
        artist_names = ', '.join(artists)
        song_list.append((track_name+artist_names))
    
################################Server Side#############################################
# Define playlist URL
from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from fastapi.responses import StreamingResponse
import requests
import io
from io import BytesIO

app = FastAPI()

def download_files_from_link(link: str):
    # Make a request to the provided link
    response = requests.get(link)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Assuming the content is a zip file, you can modify this based on your use case
        zip_content = BytesIO(response.content)
        return zip_content
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch files from the provided link")

@app.post("/download-from-link")
async def download_from_link(link: str = Form(...)):
    try:
        zip_content = download_files_from_link(link)
        return StreamingResponse(io.BytesIO(zip_content), media_type="application/zip", headers={"Content-Disposition": "attachment;filename=downloaded_files.zip"})
    except HTTPException as e:
        return e



song_list = []

get_playlist_tracks(Playlist_url, song_list)

song_name_lists = [song.replace(" ", "+") for song in song_list]
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


if __name__ == "__main__":
    for idx,url in enumerate(youtube_url_lists):
        print(f"Downloading {idx+1}/{len(youtube_url_lists)}: {song_name_lists[idx]}")
        download_audio(url)



