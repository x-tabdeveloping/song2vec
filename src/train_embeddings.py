import os
from utils.streams import json_stream, playlist_stream
from gensim.models.word2vec import Word2Vec

DATA_PATH = "../dat/playlists/data"
SAVE_PATH = "../dat/models/word2vec.model"


def main() -> None:
    data_stream = json_stream(DATA_PATH, verbose=True)
    playlists = playlist_stream(data_stream)
    model = Word2Vec(sentences=playlists)
    model.save(SAVE_PATH)


if __name__ == "__main__":
    main()
