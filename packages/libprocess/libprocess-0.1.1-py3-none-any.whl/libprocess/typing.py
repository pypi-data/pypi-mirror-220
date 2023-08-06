"""
Type declarations for collected data.
"""

from typing import List, Tuple, TypedDict, Union
from typing_extensions import NotRequired


class TimePoint(TypedDict):
    """The time point data structure."""

    year: int
    month: NotRequired[int]
    day: NotRequired[int]


class Source(TypedDict):
    """
    Attributes
    ----------
    name : str
        The name of the data source where the metadata is collected.
    url : str
        The url where the metadata is collected.
    accessDate: str
        The time (UTC+0) the entry is saved (in ISO 8601 format).
    """

    name: str
    url: str
    accessDate: str


class BaseProcessedMetadataEntry(TypedDict):
    """
    The data structure of an entry of processed metadata.

    Attributes
    ----------
    uuid : str
        The UUID of the metadata entry.
        This UUID can be used to associate the processed metadata entry
        with the corresponding metadata entry.
    authors : Union[List[str], None]
        The authors of the visualization.
        Store None if unknown.
    displayName : str
        A short title for display.
    publishDate : Union[TimePoint, List[TimePoint], None]
        The time the visualization is published.
        If the exact time is unknown, can store a time range.
        Store the year, month, day if known.
        Store None if unknown.
    viewUrl : str
        The url where the item can be viewed in a browser.
    downloadUrl : str
        The url where the item can be downloaded with a get request.
        DownloadUrl can serve the purpose of viewUrl,
        while viewUrl may not always be the same as downloadUrl,
        because some data sources provide web-based viewing functions.
    md5 : str
        The MD5 hash of the image.
    phash : str
        The perceptual hash of the visualization image.
    resolution : Tuple[int, int]
        The (width, height) of the image in pixels.
    fileSize: int
        The storage size of the image in bytes.
    languages : Union[List[str], None]
        The languages used in the visualization.
        Store the language name in ISO 639-3 codes.
        Store None if unknown.
    tags : List[str]
        The tags of the item to be used for searching.
        When no tag is available, store empty array.
    abstract : Union[str, None]
        A brief description of the visualization.
        Store null if unknown.
    rights : CopyrightStatus
        The copyright status of the image.
    source : Source
        The data source information.
    """

    uuid: str
    authors: Union[List[str], None]
    displayName: str
    publishDate: Union[TimePoint, List[TimePoint], None]
    viewUrl: str
    downloadUrl: str
    languages: Union[List[str], None]
    tags: List[str]
    abstract: Union[str, None]
    rights: str
    source: Source


class ProcessedMetadataEntry(BaseProcessedMetadataEntry):
    """
    The data structure of an entry of processed metadata.

    Attributes
    ----------
    md5 : str
        The MD5 hash of the image.
    phash : str
        The perceptual hash of the visualization image.
    resolution : Tuple[int, int]
        The (width, height) of the image in pixels.
    fileSize: int
        The storage size of the image in bytes.
    """

    md5: str
    phash: str
    resolution: Tuple[int, int]
    fileSize: int
