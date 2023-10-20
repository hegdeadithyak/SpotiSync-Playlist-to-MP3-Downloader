import requests
from bs4 import BeautifulSoup

# Replace this URL with the actual URL of your Spotify playlist
url = "https://open.spotify.com/playlist/2UT2q9QKe44zTsHzRu7cr3?si=8f8e715acff0497e&nd=1"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())
    # Extract song names using the appropriate HTML tags and attributes
    song_elements = soup.find_all('div','span','a', class_='standalone-ellipsis-one-line')  # Replace with the correct class or tag name
    
    # Extract and print the song names
    song_names = [song.text for song in song_elements]
    
    for index, song_name in enumerate(song_names):
        print(f"{index + 1}. {song_name}")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
