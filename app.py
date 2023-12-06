import os
import re
import sys
import urllib.request
from pytube import YouTube
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Get the client_id from environment variables
client_id = "535e76588a5b4c6db491cd633213c3ec"
client_secret = "3ffeca84b6084f47aeb4f2be647b0df0"

# FastAPI configuration
app = FastAPI()

# Templates configuration
templates = Jinja2Templates(directory="templates")


class Item(BaseModel):
    playlist_url: str


def download_audio(video_url, save_directory):
    video = YouTube(video_url)
    audio = video.streams.filter(only_audio=True).first()
    try:
        audio.download(save_directory)
        # Install the downloaded audio file
        os.system(f"start {os.path.join(save_directory, audio.title)}.webm")
    except Exception as e:
        print(f"Failed to download audio: {e}")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download", response_class=HTMLResponse)
async def download_songs(item: Item):
    # Spotify client setup
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
    )

    # Define the playlist URL
    playlist_url = item.playlist_url

    song_list = []
    # Extract the playlist ID from the URL
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results = sp.user_playlist_tracks("spotify", playlist_id)

    for track in results["items"]:
        track_info = track["track"]
        track_name = track_info["name"]
        artists = [artist["name"] for artist in track_info["artists"]]
        artist_names = ", ".join(artists)
        song_list.append((track_name + artist_names))

    song_name_lists = [song.replace(" ", "+") for song in song_list]

    youtube_url_lists = []
    for song_name in song_name_lists:
        song_link = f"https://www.youtube.com/results?search_query={song_name}"
        song_link = song_link.encode("ascii", "ignore").decode("ascii")
        html = urllib.request.urlopen(song_link)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = f"https://www.youtube.com/watch?v={video_ids[0]}"
        youtube_url_lists.append(url)

    for idx, url in enumerate(youtube_url_lists):
        print(f"Downloading {idx + 1}/{len(youtube_url_lists)}: {song_name_lists[idx]}")
        download_audio(url, sys.argv[2])

    return templates.TemplateResponse(
        "download.html", {"request": Request, "songs": song_name_lists}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
