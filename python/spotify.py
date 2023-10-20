import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

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
    


