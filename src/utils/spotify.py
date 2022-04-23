import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from utils.types import Track

_spotify_client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())


def fetch_track_metadata(track_uri: str) -> Track:
    """
    Fetches metadata of a certain track from Spotify.

    Parameters
    ----------
    track_uri: str
        Spotify uri of the track

    Returns
    ----------
    track: Track
        Track object
    """
    spotify_track = _spotify_client.track(track_id=track_uri)
    track_name = spotify_track["name"]
    album_name = spotify_track["album"]["name"]
    associated_genres = []
    artist_names = []
    for artist in spotify_track["artists"]:
        artist = _spotify_client.artist(artist["uri"])
        artist_names.append(artist["name"])
        # print(artist)
        if "genres" in artist:
            associated_genres.extend(artist["genres"])
    genres = ", ".join(associated_genres)
    artists = ", ".join(artist_names)
    track: Track = {
        "track_uri": track_uri,
        "track_name": track_name,
        "album_name": album_name,
        "genres": genres,
        "artists": artists,
    }
    return track
