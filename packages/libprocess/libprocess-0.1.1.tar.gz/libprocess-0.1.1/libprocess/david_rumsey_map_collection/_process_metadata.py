"""
Process metadata.

TODO: check if the following data attributes can be used
- sourceData:
    - iiifManifest
    - fieldValues
        - 'Author'
        - 'Date'
        - 'Short Title'
        - 'Publisher'
        - 'Publisher Location' 
        - 'Obj Height cm'
        - 'Obj Width cm'
        - 'Scale 1'
        - 'Engraver or Printer'
        - 'World Area'
        - 'Full Title'
        - 'Page No'
        - 'Pub Height cm'
        - 'Pub Width cm'
        - 'Download 1'
        - 'Download 2'
        - 'Authors'
"""

from typing import Any, Dict, List, Union

from libquery.david_rumsey_map_collection._typing import (
    MetadataEntry,
    SourceData,
)
from libquery.utils.jsonl import load_jl
from tqdm import tqdm

from ..typing import BaseProcessedMetadataEntry
from .._utils.image import (
    get_md5_by_uuid,
    get_phash_by_uuid,
    get_shape_by_uuid,
    get_storage_size_by_uuid,
)
from .._utils.language import detect_iso6393


def get_attr(field_values: List[Dict[str, List]], key: str) -> Union[List, None]:
    d = next((d for d in field_values if key in d), None)
    return d[key] if d is not None else None


def get_first_element(a: Union[List, None]) -> Union[Any, None]:
    if (a is None) or (len(a) == 0):
        return None
    return a[0]


def get_authors(field_values: List[Dict]) -> Union[List[str], None]:
    authors: Union[List[str], None] = get_attr(field_values, "Publication Author")
    return authors


def get_display_name(source_data: SourceData) -> str:
    return source_data["displayName"].replace("\u200b", "").replace("\u00a0", " ")


def get_languages_by_rules(field_values: List[Dict]) -> Union[List[str], None]:
    note = get_first_element(get_attr(field_values, "Note"))
    if note is None:
        return None

    # Rule:
    if "In both Hungarian and German" in note:
        # Hungarian, German
        return ["hun", "deu"]


def get_languages(field_values: List[Dict]) -> Union[List[str], None]:
    languages = get_languages_by_rules(field_values)
    if languages is not None:
        return languages

    publish_title = get_first_element(get_attr(field_values, "Pub Title"))
    language = detect_iso6393(publish_title)
    return None if language is None else [language]


def get_tags(field_values: List[Dict]) -> List[str]:
    tags = []
    tags_type = get_attr(field_values, "Type")
    if tags_type is not None:
        tags += tags_type
    tags_subject = get_attr(field_values, "Subject")
    if tags_subject is not None:
        tags += tags_subject
    tags_pub_type = get_attr(field_values, "Pub Type")
    if tags_pub_type is not None:
        tags += tags_pub_type

    # Discard useless tags
    useless_tags = [
        "Data Visualization",
    ]
    tags = [d for d in tags if d not in useless_tags]
    return list(set(tags))


def get_abstract(field_values: List[Dict]) -> Union[str, None]:
    note = get_first_element(get_attr(field_values, "Note"))
    if note is None:
        return note
    return note.replace("\u200b", "").replace("\u00a0", " ")


def process(
    entry: MetadataEntry, img_dir: Union[str, None]
) -> BaseProcessedMetadataEntry:
    """
    Postprocess a metadata entry.
    If img directory is not provided, do not compute the image attributes.
    """

    id_in_source = entry["idInSource"]
    source_data = entry["sourceData"]

    source_data_id = source_data["id"]
    field_values = source_data["fieldValues"]

    # store size4 if exist and size2 otherwise
    download_url: str = (
        source_data["urlSize4"]
        if "urlSize4" in source_data
        else source_data["urlSize2"]
    )

    image_attributes = (
        {}
        if img_dir is None
        else {
            "md5": get_md5_by_uuid(entry["uuid"], img_dir),
            "phash": get_phash_by_uuid(entry["uuid"], img_dir),
            "resolution": get_shape_by_uuid(entry["uuid"], img_dir),
            "fileSize": get_storage_size_by_uuid(entry["uuid"], img_dir),
        }
    )

    return {
        "uuid": entry["uuid"],
        "authors": get_authors(field_values),
        "displayName": get_display_name(source_data),
        "publishDate": {
            "year": int(get_first_element(get_attr(field_values, "Pub Date"))),
        },
        "viewUrl": f"https://www.davidrumsey.com/luna/servlet/detail/{source_data_id}",
        "downloadUrl": download_url,
        **image_attributes,
        "languages": get_languages(field_values),
        "tags": get_tags(field_values),
        # Note: all the entries have either no note (stored as None) or 1 note
        "abstract": get_abstract(field_values),
        # Reference: https://www.davidrumsey.com/about
        "rights": "CC BY-NC-SA 3.0",
        "source": {
            "name": entry["source"],
            # Note: do not use entry['url'], which is not a stable link
            "url": f"https://www.davidrumsey.com/luna/servlet/as/search?mid={id_in_source}",
            "accessDate": entry["accessDate"],
        },
        # Deprecated properties:
        # 'publisher': get_first_element(get_attr(field_values, 'Publisher')),
        # 'publisherAddress': get_first_element(get_attr(field_values, 'Publisher Location')),
        # 'publishTitle': publish_title,
        # 'publishNote': get_first_element(get_attr(field_values, 'Pub Note')),
    }


def process_batch(
    metadata_path: str, img_dir: Union[str, None]
) -> List[BaseProcessedMetadataEntry]:
    """
    Process a batch of metadata entries.
    """

    metadata = load_jl(metadata_path)
    processed_metadata = [
        process(d, img_dir) for d in tqdm(metadata, desc="Process Metadata Progress")
    ]

    if img_dir is None:
        return processed_metadata
    # Ignore the entries where the phash computation failed,
    # meaning that the corresponding image has not been fetched
    # or the fetched image is corrupted.
    return [d for d in processed_metadata if d["phash"] is not None]
