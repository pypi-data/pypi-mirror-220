"""
Process rawMetadata.jsonl and output metadata.json.

TODO: check if the following data attributes can be used
- InternetArchiveMetadata: coverage, publisher, source, year
- SourceData: d1, d2, files
"""

# pylint: disable=invalid-name

import datetime
import os
import re
from typing import List, Union

# import nltk
from html2text import HTML2Text
from libquery.utils.jsonl import load_jl
from libquery.internet_archive._fetch_file import _get_filename
from libquery.internet_archive._typing import (
    MetadataEntry,
    SourceData,
)
from libquery.internet_archive._utils import get_image_uuid
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from tqdm import tqdm
from zipfile import ZipFile

from ..typing import (
    BaseProcessedMetadataEntry,
    TimePoint,
)
from .._utils.image import (
    get_md5_by_path,
    get_phash_by_path,
    get_shape_by_path,
    get_storage_size_by_path,
)
from .._utils.language import detect_iso6393

# nltk.download('punkt', quiet=True)
# nltk.download('averaged_perceptron_tagger', quiet=True)
# nltk.download('maxent_ne_chunker', quiet=True)
# nltk.download('words', quiet=True)


def is_name(text: str) -> bool:
    chunks = ne_chunk(pos_tag(word_tokenize(text)))
    for chunk in chunks:
        if type(chunk) != Tree:
            continue
        if chunk.label() == "PERSON":
            return True
    return False


def get_authors(source_data: SourceData) -> List[str]:
    if "creator" not in source_data["metadata"]:
        return []
    creator = source_data["metadata"]["creator"]
    creators = creator if isinstance(creator, list) else [creator]

    authors = []
    for creator in creators:
        authors += creator.split("; ")
    return authors


def parse_date(date: str) -> Union[TimePoint, None]:
    if date == "0000":
        return None

    m = re.findall(r"^\d{1,4}$", date)
    if len(m) == 1:
        return {"year": int(date)}

    m = re.findall(r"^\d{1,2}\/\d{1,2}\/\d{4}$", date)
    if len(m) == 1:
        date_obj = datetime.datetime.strptime(date, "%m/%d/%Y")
        return {
            "year": date_obj.year,
            "month": date_obj.month,
            "day": date_obj.day,
        }

    m = re.findall(r"^\d{4}-\d{2}-\d{2}$", date)
    if len(m) == 1:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        return {
            "year": date_obj.year,
            "month": date_obj.month,
            "day": date_obj.day,
        }

    m = re.findall(r"\d{1,4}", date)
    if len(m) == 1:
        return {"year": int(m[0])}

    return None


def get_publish_date(source_data: SourceData) -> Union[TimePoint, None]:
    if "date" not in source_data["metadata"]:
        return None
    date = source_data["metadata"]["date"]
    if isinstance(date, list):
        time_points = [parse_date(d) for d in date]
        return next(d for d in time_points if d is not None)
    return parse_date(date)


def get_tags(source_data: SourceData) -> List[str]:
    metadata = source_data["metadata"]
    if "subject" not in metadata:
        return []

    tags = []
    subject = metadata["subject"]
    tags_subject = subject if isinstance(subject, list) else [subject]
    for tag in tags_subject:
        parts = [d.lstrip("* ").rstrip("; ").title() for d in tag.split(";")]
        tags += [d for d in parts if d != "" and not is_name(d)]

    return list(set(tags))


def get_languages(source_data: SourceData) -> Union[List[str], None]:
    language = detect_iso6393(source_data["metadata"]["title"])
    return None if language is None else [language]


def get_abstract(source_data: SourceData) -> Union[str, None]:
    if "description" not in source_data["metadata"]:
        return None
    description = source_data["metadata"]["description"]
    if isinstance(description, str):
        return HTML2Text(bodywidth=0).handle(description)
    return " ".join([HTML2Text(bodywidth=0).handle(d) for d in description])


def get_rights(source_data: SourceData) -> str:
    if "rights" not in source_data["metadata"]:
        return "unknown"
    rights = source_data["metadata"]["rights"]
    mapping = {
        "Public Domain": "public domain",
        '<a href="http://creativecommons.org/publicdomain/mark/1.0/" rel="nofollow">This work is available under the Creative Commons, Public Domain Mark</a>': "public domain",
        "FREE": "public domain",
        "The contributing institution believes that this item is not in copyright": "public domain",
        "The contributing institution believes that this item is not in copyright.": "public domain",
        '<a href="https://rightsstatements.org/page/InC/1.0/?language=en" rel="nofollow">It is possible this Item is protected by copyright and/or related rights. You are free to use this Item in any way that is permitted by the copyright and related rights legislation that applies to your use. For other uses you need to obtain permission from the rights-holder(s).</a>': "restricted use",
    }
    return mapping[rights]


def get_download_url_for_image_in_zip(
    zip_filename: str, image_filename: str, source_data: SourceData
) -> str:
    server = source_data["server"]
    query_extension = "&ext=jpg" if image_filename.endswith(".jp2") else ""
    return f'https://{server}/view_archive.php?archive={source_data["dir"]}/{zip_filename}&file={zip_filename.replace(".zip", "")}%2F{image_filename}{query_extension}'


def filename2uuid(filename: str) -> str:
    return filename.split(".")[0]


def postprocess(
    entry: MetadataEntry, download_dir: str, img_dir: Union[str, None]
) -> List[BaseProcessedMetadataEntry]:
    """
    Postprocess a raw metadata entry.
    If img directory is not provided, do not compute the image attributes.
    """

    id_in_source = entry["idInSource"]
    source_data = entry["sourceData"]
    identifier = source_data["metadata"]["identifier"]
    filename = _get_filename(source_data)
    if filename is None:
        return []

    partial_entry = {
        "authors": get_authors(source_data),
        "publishDate": get_publish_date(source_data),
        "languages": get_languages(source_data),
        "tags": get_tags(source_data),
        "abstract": get_abstract(source_data),
        "rights": get_rights(source_data),
        "source": {
            "name": entry["source"],
            # Note: do not use entry['url'], which is not a stable link
            "url": f"https://archive.org/search?query=identifier:({id_in_source})",
            "accessDate": entry["accessDate"],
        },
    }

    # TODO: utilize the information about files and page number in the raw metadata
    # instead of relying solely on the zip files.
    # In this way, the metadata can be computed for the entries
    # whose files have not yet been downloaded.

    # Check whether the file is a single image or a collection of images.
    if filename.endswith(".zip"):
        path = f"{download_dir}/{id_in_source}/{filename}"
        if not os.path.exists(path):
            return []
        with ZipFile(path, "r") as zip_ref:
            relative_paths = zip_ref.namelist()
        image_filenames = [
            d.split("/")[1] for d in relative_paths if not d.endswith("/")
        ]
        entries = []
        uuid2filename = {filename2uuid(d): d for d in os.listdir(img_dir)}
        for image_filename in image_filenames:
            uuid = get_image_uuid(image_filename, entry["source"])
            if (img_dir is not None) and (uuid not in uuid2filename):
                continue
            page_index = int(image_filename.split(".")[0].split("_")[-1])

            if img_dir is None:
                image_attributes = {}
            else:
                image_path = f"{img_dir}/{uuid2filename[uuid]}"
                image_attributes = {
                    "md5": get_md5_by_path(image_path),
                    "phash": get_phash_by_path(image_path),
                    "resolution": get_shape_by_path(image_path),
                    "fileSize": get_storage_size_by_path(image_path),
                }

            entries.append(
                {
                    **partial_entry,
                    "uuid": uuid,
                    "displayName": source_data["metadata"]["title"]
                    + f" - Page {page_index}",
                    "viewUrl": f"https://archive.org/details/{identifier}/page/n{page_index}",
                    # 'downloadUrl': f'https://archive.org/download/{identifier}/{filename}',
                    "downloadUrl": get_download_url_for_image_in_zip(
                        filename, image_filename, source_data
                    ),
                    **image_attributes,
                }
            )
        return entries
    else:
        if img_dir is None:
            image_attributes = {}
        else:
            image_path = f"{download_dir}/{identifier}/{filename}"
            image_attributes = {
                "md5": get_md5_by_path(image_path),
                "phash": get_phash_by_path(image_path),
                "resolution": get_shape_by_path(image_path),
                "fileSize": get_storage_size_by_path(image_path),
            }

        return [
            {
                **partial_entry,
                "uuid": get_image_uuid(filename, entry["source"]),
                "displayName": source_data["metadata"]["title"],
                "viewUrl": f"https://archive.org/details/{identifier}",
                "downloadUrl": f"https://archive.org/download/{identifier}/{filename}",
                **image_attributes,
            }
        ]


def postprocess_batch(
    raw_metadata_path: str, download_dir: str, img_dir: Union[str, None]
) -> List[BaseProcessedMetadataEntry]:
    """
    Postprocess a batch of raw metadata entries.
    """

    raw_metadata = load_jl(raw_metadata_path)
    metadata = []
    for d in tqdm(raw_metadata, desc="Process Metadata Progress"):
        metadata += postprocess(d, download_dir, img_dir)

    if img_dir is None:
        return metadata
    # Ignore the entries where the phash computation failed,
    # meaning that the corresponding image has not been crawled
    # or the crawled image is corrupted.
    return [d for d in metadata if d["phash"] is not None]
