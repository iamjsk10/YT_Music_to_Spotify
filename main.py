import os

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pytube import Playlist


load_dotenv()
# spotify id and secret
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def create_song_list(playlist_url):
    songList = []
    playlist = Playlist(playlist_url)
    for video in playlist.videos:
        songList.append(video.title)
    print(len(songList))
    print(" songs read from the playlist")
    return songList

#           --- spotify Part ---

def get_token():
    # Initialize Spotipy with OAuth token
    sp_oauth = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri="http://localhost:8080",
                            scope="playlist-modify-public playlist-modify-private")
    token_info =sp_oauth.get_cached_token()
    return token_info['access_token']


def get_user_profile(token):
    # Initialize Spotipy with OAuth token
    sp = spotipy.Spotify(auth=token)
    user_data = sp.current_user()
    user_id = user_data['id']
    return user_id


def search_for_track(token, track_name):

    sp = spotipy.Spotify(auth=token)
    # Search for tracks
    results = sp.search(q=f"track:{track_name} ", limit=1)
    tracks = results['tracks']['items']
    if tracks:
       return tracks[0]["uri"]
    else:
         print("No Track found with name " + track_name)

# takes in token and list of track names
def search_for_multiple_tracks(token, playlist_data):
    print("Searching for tracks...")
    sp = spotipy.Spotify(auth=token)
    track_list = []

    for track_name in playlist_data:
        # Perform actions on each video title
        if '(' in track_name:
            index = track_name.index('(')
            track_name = track_name[:index].strip()
        if '[' in track_name:
            index = track_name.index('[')
            track_name = track_name[:index].strip()
        results = search_for_track(token,track_name)
        if(results!=None):
            track_list.append(results)
    return track_list

def create_playlist(username, playlist_name, playlist_description,token):
    sp = spotipy.Spotify(auth=token)
    # Create playlist
    playlist = sp.user_playlist_create(user=username, name=playlist_name, public=False,
                                       description=playlist_description)
    playlist_id = playlist['id']
    print("Playlist created successfully!")
    return playlist_id

def add_tracks_to_playlist(token, user_profile, playlist_id, track_list):
    print("Adding tracks to playlist")
    sp = spotipy.Spotify(auth=token)
    # add items takes list!!!!! Not single URIs
    length=len(track_list)
    print(str(length) + " tracks to be added to the playlist")
    begin=0
    end = 49
    count=1
    while(end<=length):
        sp.playlist_add_items(playlist_id,track_list[begin:end])
        begin = end
        if (length -end<50):
            end = length
        else:
            end+=50
        count += 1

def main():
    playlist_url = "ENTER_URL_OF_YOUR_PLAYLIST" # doesn't have to be public, shared links work as well
    token = get_token()
    user_profile = get_user_profile(token)
    video_list = create_song_list(playlist_url)
    new_playlist = create_playlist(user_profile, "ENTER_NAME_FOR_SPOTIFY_PLAYLIST", "",token)
    generated_ids = search_for_multiple_tracks(token, video_list);
    add_tracks_to_playlist(token, user_profile, new_playlist, generated_ids)

if __name__ == "__main__":
    main()



