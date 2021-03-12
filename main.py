import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = "a5247c60d2ed4a3f9e2423cc81f86ea3"
SPOTIPY_CLIENT_SECRET = "97aace7861e54c719a881769cf0cf3c8"
SPOTIPY_REDIRECT_URI = "http://example.com"

#span class: "chart-element__information__song text--truncate color--primary"

billboard_date = input("Please provide the date you'd like songs from (yyyy-mm-dd): ")
date_list = billboard_date.split("-")
print(date_list)
billboard_url = "https://www.billboard.com/charts/hot-100/" + billboard_date

response = requests.get(billboard_url)

billboard_page = response.text
soup = BeautifulSoup(billboard_page, "html.parser")

songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_list = [song.text for song in songs]
print(song_list)

#------------Spotipy quick start------------------
spotify_auth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope="playlist-modify-private", username="ryan.szotak@gmail.com")
user_client = spotipy.client.Spotify(auth_manager=spotify_auth)
#print(user_client.current_user()["id"])

track_uri_list = []
for i in song_list:
    try:
        track_search = user_client.search(q=f"track: {i} year: {date_list[0]}", type="track")
        track_uri_list.append(track_search["tracks"]["items"][0]["uri"])
    except IndexError:
        print("Track doesn't exist in Spotify, skipping!")

print(track_uri_list)

playlist_id = user_client.user_playlist_create(user=user_client.current_user()["id"],name=f"{billboard_date} Billboard Top 100",public=False)["id"]

user_client.playlist_add_items(playlist_id=playlist_id, items=track_uri_list)
