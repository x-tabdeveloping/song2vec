"""
Module containing methods for streaming data from the dataset.
"""
from itertools import islice
import json
import os
from typing import Callable, Iterable, List, Tuple, TypeVar


def reusable(gen_func: Callable) -> Callable:
    """
    Function decorator that turns your generator function into an
    iterator, thereby making it reusable.

    Parameters
    ----------
    gen_func: Callable
        Generator function, that you want to be reusable
    Returns
    ----------
    _multigen: Callable
        Sneakily created iterator class wrapping the generator function
    """

    class _multigen:
        def __init__(self, *args, limit=None, **kwargs):
            self.__args = args
            self.__kwargs = kwargs
            self.limit = limit

        def __iter__(self):
            if self.limit is not None:
                return islice(gen_func(*self.__args, **self.__kwargs), self.limit)
            return gen_func(*self.__args, **self.__kwargs)

    return _multigen


T = TypeVar("T")


@reusable
def with_progress(items: List[T]) -> Iterable[Tuple[float, T]]:
    """
    Wraps list in an iterable that streams the progress percentage alongside with
    the items.

    Parameters
    ----------
    items: list of T
        Items to iterate over

    Yields
    ----------
    progress: float
        Progress in %
    item: T
        Current item under processing
    """
    total = len(items)
    for iteration, item in enumerate(items):
        progress = 100 * (iteration / float(total))
        yield progress, item


T = TypeVar("T")


@reusable
def progress_bar_stream(items: List[T]) -> Iterable[T]:
    """
    Wraps list in an iterable that shows a progress bar and the current element.

    Parameters
    ----------
    items: List[T]
        Items to iterate over (of type T)

    Yields
    ----------
    item: T
        Current item under processing
    """
    BAR_LENGTH = 100
    N_DECIMALS = 1
    FILL_CHARACTER = "█"
    for progress, item in with_progress(items):
        filledLength = int(BAR_LENGTH * progress // 100)
        bar = FILL_CHARACTER * filledLength + "-" * (BAR_LENGTH - filledLength)
        os.system("clear")
        print(f"Progress: |{bar}| {progress}% \n Current item processed: {item}\n")
        yield item


@reusable
def json_stream(data_path: str, verbose: bool = True) -> Iterable[dict]:
    """
    Parses and streams all json files from the given path.

    Parameters
    ----------
    data_path: str
        Path to stream the data from
    verbose: bool, default True
        If set to True the stream will display a progress bar and the name of the current file in processing.

    Yields
    ----------
    json_object: dict
        The parsed JSON object for each file
    """
    for root, dirs, files in os.walk(data_path):
        if verbose:
            files = progress_bar_stream(files)
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                with open(file_path, encoding="UTF-8") as file:
                    yield json.load(file)


@reusable
def playlist_stream(data_stream: Iterable[dict]) -> Iterable[List[str]]:
    """
    Streams all playlists in the form of lists song names from a given json stream.

    Parameters
    ----------
    data_stream: Iterable[dict]
        JSON stream of parsed files

    Yields
    ----------
    songs: List[str]
        List of track uris in the current playlist.
    """
    for json_object in data_stream:
        for playlist in json_object["playlists"]:
            yield [track["track_uri"] for track in playlist["tracks"]]
