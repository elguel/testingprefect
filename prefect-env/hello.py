from prefect import flow, task
from prefect.blocks.system import String
from credentials import cid, secret
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd 

from prefect.blocks.system import Secret

#cid = Secret.load("cid")
#secret = Secret.load("client-secret")

@task
def spotify_connect():
  client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
  sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
  return sp

@flow
def extract(playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"):
  sp=spotify_connect()
  playlist_URI = playlist_link.split("/")[-1].split("?")[0]
  #track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

  my_dict = {"track_uri":[],"track_name":[],"artist_uri":[]
           ,"artist_info":[],"artist_name":[],
           "artist_pop":[],"artist_genres":[]
           ,"album":[],"track_pop":[]}

  for track in sp.playlist_tracks(playlist_URI)["items"]:
      #URI
      track_uri = track["track"]["uri"]
      
      #Track name
      track_name = track["track"]["name"]
      
      #Main Artist
      artist_uri = track["track"]["artists"][0]["uri"]
      artist_info = sp.artist(artist_uri)
      
      #Name, popularity, genre
      artist_name = track["track"]["artists"][0]["name"]
      artist_pop = artist_info["popularity"]
      artist_genres = artist_info["genres"]
      
      #Album
      album = track["track"]["album"]["name"]
      
      #Popularity of the track
      track_pop = track["track"]["popularity"]
  
      
      my_dict["track_uri"].append(track_uri)
      my_dict["track_name"].append(track_name)
      my_dict["artist_uri"].append(artist_uri)
      my_dict["artist_info"].append(artist_info)
      my_dict["artist_name"].append(artist_name)
      my_dict["artist_pop"].append(artist_pop)
      my_dict["artist_genres"].append(artist_genres)
      my_dict["album"].append(album)
      my_dict["track_pop"].append(track_pop)


      df = pd.DataFrame(my_dict)
      return df

if __name__ == "__main__":
    df=extract()
    print(df)