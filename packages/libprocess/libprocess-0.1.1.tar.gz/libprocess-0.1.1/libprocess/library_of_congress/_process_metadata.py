"""
Process metadata.

TODO: check if the following data attributes can be used
- SourceData
    - resources
    - segments
    - related
    - access_restricted
    - extract_timestamp
    - group
    - hassegments
    - mime_type
    - online_format
    - original_format
    - shelf_id
    - timestamp
    - location
    - number
    - number_source_modified
    - number_lccn
    - number_oclc
    - subject
    - contributor
    - location_country
    - location_county
    - location_state
    - location_city
    - type
    - partof
- Item
    - image resources: service_low, service_medium, thumb_gallery
    - ids: digital_id, control_number, call_number, id
    - properties that may have be duplicated in SourceData: language, title, date
    - others:
        - access_advisory, repository, location, medium, other_title,
        - source_collection, subjects, translated_title, 
        - contents, creator, summary, related_items,
        - created, created_published_date, creators,
        - display_offsite, formats, link, medium_brief, mediums,
        - modified, resource_links, sort_date,
        - source_created, source_modified, subject_headings
"""

import re
import textwrap
from typing import List, Union
from datetime import datetime

import langcodes
from libquery.library_of_congress._typing import (
    MetadataEntry,
    SourceData,
)
from libquery.utils.jsonl import load_jl
from tqdm import tqdm

from ..typing import BaseProcessedMetadataEntry, TimePoint
from .._utils.image import (
    get_md5_by_uuid,
    get_phash_by_uuid,
    get_shape_by_uuid,
    get_storage_size_by_uuid,
)


def parse_date(date: str) -> Union[TimePoint, None]:
    digits = "".join(re.findall(r"\d+", date))
    if len(digits) <= 3:
        return None
    if date.count("-") == 0:
        if int(date) > 2023:
            return None
        return {"year": int(date)}
    if date.count("-") == 1:
        date_obj = datetime.strptime(date, "%Y-%m")
        if date_obj.year > 2500:
            print(date_obj.year)
        return {
            "year": date_obj.year,
            "month": date_obj.month,
        }
    if date.count("-") == 2:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        return {
            "year": date_obj.year,
            "month": date_obj.month,
            "day": date_obj.day,
        }
    return None


def parse_created_published(date: str) -> Union[TimePoint, None]:
    segment = date.split(", ")[-1]
    digits = "".join(re.findall(r"\d+", segment))[:4]
    digits_pre = "".join(re.findall(r"\d+", segment[:4]))
    if len(digits) == 4 or len(digits_pre) == 4:
        return {"year": int(digits)}
    return None


def get_publish_date(source_data: SourceData) -> Union[TimePoint, None]:
    if "date" in source_data:
        date = parse_date(source_data["date"])
        if date is not None:
            return date
    if "created_published" in source_data["item"]:
        created_published = source_data["item"]["created_published"]
        if isinstance(created_published, list):
            created_published = created_published[0]
        return parse_created_published(created_published)
    return None


def search_ISO_639_3(language_str: str) -> Union[str, List[str], None]:
    try:
        return langcodes.find(language_str).to_alpha3()
    except LookupError:
        if len(language_str) % 3 != 0:
            return None

        # Handle cases like 'engchi' (interpreted as ['English', 'Chinese'])
        parts = textwrap.wrap(language_str, 3)
        is_valid = [langcodes.tag_is_valid(part) for part in parts]
        if False in is_valid:
            return None
        return parts


def get_languages(source_data: SourceData) -> List[str]:
    if "language" not in source_data:
        return []

    languages = source_data["language"]
    if not isinstance(languages, list):
        languages = [languages]

    parsed = []
    for d in languages:
        matched = search_ISO_639_3(d)
        if isinstance(matched, str):
            parsed.append(matched)
        elif isinstance(matched, list):
            parsed += matched
        else:
            parsed.append(d)
    return [*set(parsed)]


def get_abstract(source_data: SourceData) -> Union[str, None]:
    if "description" in source_data:
        return " ".join(source_data["description"])
    if "notes" in source_data["item"]:
        return " ".join(source_data["item"]["notes"])
    return None


def get_tags(source_data: SourceData) -> List[str]:
    tags = []
    if "format" in source_data:
        tags += source_data["format"]
    if "genre" in source_data:
        tags += source_data["genre"]
    return tags


def clean_rights(rights: str) -> str:
    no_known_restrictions_flags = [
        "No known restrictions",
        "No known copyright restrictions on publication.",
    ]
    for d in no_known_restrictions_flags:
        if d in rights:
            return "no known restrictions"

    in_copyright_flags = [
        "May be restricted",
        "Publication may be restricted.",
        "Publication restricted.",
        "For rights information",
        "For rights relating to this resource",
    ]
    for d in in_copyright_flags:
        if d in rights:
            return "restricted use"

    not_evaluated_flags = [
        "Rights status not evaluated",
        "Rights status of individual images not evaluated.",
        "The rights status of this item has not been evaluated.",
    ]
    for d in not_evaluated_flags:
        if d in rights:
            return "unknown"

    # NOTE: the copyright information that fails
    # to match the template is regarded unknown.
    return "unknown"


def get_rights(source_data: SourceData) -> str:
    """
    Extracts rights information from
    rights, rights_advisory, rights_information.
    """

    item = source_data["item"]

    rights = []

    if "rights" in item:
        rights.append(item["rights"])

    if "rights_advisory" in item:
        rights_advisory = item["rights_advisory"]
        if not isinstance(rights_advisory, list):
            rights_advisory = [rights_advisory]
        rights += rights_advisory

    if "rights_information" in item:
        rights.append(item["rights_information"])

    rights = [*set(rights)]

    assert len(rights) <= 1, f"Unexpected rights with length > 1: {rights}"

    if len(rights) == 0:
        return "unknown"
    return clean_rights(rights[0])


def process(
    entry: MetadataEntry, img_dir: Union[str, None]
) -> BaseProcessedMetadataEntry:
    """
    Postprocess a metadata entry.
    If img directory is not provided, do not compute the image attributes.
    """

    source_data = entry["sourceData"]
    item = source_data["item"]

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
        "authors": item.get("contributors", None),
        "displayName": source_data["title"],
        "publishDate": get_publish_date(source_data),
        "viewUrl": source_data["url"],
        # Note: the image_url stores URLs of the image with different resolution.
        # The last entry of the image_url gives the highest resolution.
        "downloadUrl": source_data["image_url"][-1],
        **image_attributes,
        "languages": get_languages(source_data),
        "tags": get_tags(source_data),
        "abstract": get_abstract(source_data),
        "rights": get_rights(source_data),
        "source": {
            "name": entry["source"],
            "url": entry["url"],
            "accessDate": entry["accessDate"],
        },
    }


def process_batch(
    metadata_path: str, img_dir: Union[str, None]
) -> List[BaseProcessedMetadataEntry]:
    """
    Postprocess a batch of metadata entries.
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
    processed_metadata = [d for d in processed_metadata if d["phash"] is not None]
    processed_metadata = {d["uuid"]: d for d in processed_metadata}
    return [*processed_metadata.values()]
