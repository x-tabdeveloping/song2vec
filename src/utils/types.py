"""
Module containing all type definitions used in other parts of the project :)
"""

from typing import TypedDict


class Track(TypedDict):
    """
    Wrapper class for annotating the type of tracks in the dataset.

    Attributes
    ----------
    track_uri: str
        Spotify uri of a track, unique identifier
    track_name: str
        Name of the track
    album_name: str
        Name of the album the track is from
    genres: str
        Genres associated with the artists of the track (comma separated)
    artists: str
        Names of artists associated with the track (comma separated)
    """

    track_uri: str
    track_name: str
    album_name: str
    genres: str
    artists: str
