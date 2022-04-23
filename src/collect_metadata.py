from gensim.models.word2vec import Word2Vec
import pandas as pd
import csv
from utils.notify import send_message

from utils.spotify import fetch_track_metadata
from utils.streams import progress_bar_stream, with_progress

DATA_PATH = "../dat/playlists/data"
SAVE_PATH = "../dat/models/word2vec.model"
METADATA_PATH = "../dat/metadata/track_metadata.tsv"


def initialise_metadata_file(path: str) -> None:
    with open(path, "wt") as metadata_file:
        tsv_writer = csv.writer(metadata_file, delimiter="\t")
        tsv_writer.writerow(
            ["track_uri", "track_name", "album_name", "genres", "artists"]
        )


def write_track(tsv_writer: csv.writer, track_uri: str) -> None:  # type: ignore
    try:
        record = fetch_track_metadata(track_uri=track_uri)
        tsv_writer.writerow(
            [
                record["track_uri"],
                record["track_name"],
                record["album_name"],
                record["genres"],
                record["artists"],
            ]
        )
    except Exception:
        print(f"Metadata could not be fetched for the track: {track_uri}")


def main() -> None:
    print("----Loading Word2Vec Model----")
    model = Word2Vec.load(SAVE_PATH)
    vocabulary = model.wv.key_to_index
    print("----Checking metadata file----")
    try:
        metadata_df = pd.read_csv(METADATA_PATH, delimiter="\t")
        print("    Metadata file already exists, appending.")
        already_done = set(metadata_df["track_uri"].unique())
    except FileNotFoundError:
        print("    Metadata file does not exist, creating a new one.")
        initialise_metadata_file(METADATA_PATH)
        already_done = set([])
    print("----Starting to fetch metadata----")
    total = len(vocabulary)
    percent = total // 100
    with open(METADATA_PATH, "at") as metadata_file:
        tsv_writer = csv.writer(metadata_file, delimiter="\t")
        for i, track_uri in enumerate(vocabulary):
            if track_uri not in already_done:
                write_track(tsv_writer, track_uri)
            if i % (percent * 5) == 0:
                progress = i // percent
                send_message(f"----Processing at {progress}%----")
        send_message("----Metadata collection DONE----")


if __name__ == "__main__":
    main()
