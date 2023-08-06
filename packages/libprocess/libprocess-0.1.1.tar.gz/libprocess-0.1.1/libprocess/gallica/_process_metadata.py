"""
Process metadata.

TODO: check if the following data attributes can be used
- Record
    - dc:source
    - dc:subject
    - dc:coverage
    - dc:publisher
    - dc:contributor
- Page
    - numero
    - pagination_type
"""

import re
from typing import Any, Dict, List, Union

from tqdm import tqdm
from libquery.gallica._typing import (
    MetadataEntry,
    Page,
    Record,
)
from libquery.utils.jsonl import load_jl

from ..typing import (
    BaseProcessedMetadataEntry,
    TimePoint,
)
from .._utils.image import (
    get_md5_by_uuid,
    get_phash_by_uuid,
    get_shape_by_uuid,
    get_storage_size_by_uuid,
)
from ._utils import (
    get_image_uuid,
    get_image_url,
    get_view_url,
)


def get_english_attr(record: Record, key: str) -> Union[List[str], None]:
    """
    Wrap the attribute value into a list and
    discard the attribute values not stored in English.
    """

    if key not in record:
        return None

    items = record[key]
    if not isinstance(items, list):
        items = [items]

    texts = []
    for item in items:
        if isinstance(item, dict) and "@xml:lang" in item:
            if item["@xml:lang"] == "eng":
                texts.append(item["#text"])
        if isinstance(item, str):
            texts.append(item)

    return texts


def get_first_element(a: Union[List, None]) -> Union[Any, None]:
    if a is None or len(a) == 0:
        return None
    return a[0]


def get_is_book(record: Record) -> bool:
    """
    Check whether an entry is a book given the 'dc:type' attribute.

    An Example of dc:type values:
    1. entry: https://gallica.bnf.fr/ark:/12148/bpt6k4804687z?lang=EN
    its "dc:type": ["text", "monographie imprimée", "printed monograph"]
    2. entry: https://gallica.bnf.fr/ark:/12148/btv1b10052128p?lang=EN
    its "dc:type": ["manuscript", "manuscrit"]
    3. entry: https://gallica.bnf.fr/ark:/12148/btv1b5901119d?lang=EN
    its "dc:type": [
        "manuscript cartographic resource",
        "document cartographique manuscrit",
        "atlas", "atlas", "map", "carte", "map", "carte", "map",
        "carte", "image fixe", "image", "still image"
    ]
    """

    types = get_english_attr(record, "dc:type")

    if types is None:
        return False

    for type_string in types:
        # A book's dc:type entry contains 'text' or 'manuscript'.
        if "manuscript" in type_string or "text" in type_string:
            return True

    return False


def get_authors(record: Record) -> Union[List[str], None]:
    creator = get_english_attr(record, "dc:creator")
    if creator is None:
        return None
    return list(set(get_english_attr(record, "dc:creator")))


def get_publish_date(record: Record) -> Union[TimePoint, None]:
    publish_year_str = get_first_element(get_english_attr(record, "dc:date"))
    if not isinstance(publish_year_str, str):
        return None

    m = re.findall(r"\d{1,4}", publish_year_str)
    if len(m) == 0:
        return None

    year = int(m[0])
    if year < 10:
        # Handle cases like '1...' (interpreted as 1000 - 1999)
        return [{"year": year * 1000}, {"year": year * 1000 + 999}]
    if year >= 10 and year < 99:
        # Handle cases like '13..' (interpreted as 1300 - 1399)
        return [{"year": year * 100}, {"year": year * 100 + 99}]
    if year >= 100 and year < 999:
        # Handle cases like '194.' (interpreted as 1940 - 1949)
        return [{"year": year * 10}, {"year": year * 10 + 9}]
    return {"year": year}


def get_languages(record: Record) -> List[str]:
    languages = get_english_attr(record, "dc:language")
    if languages is None:
        return None

    # Parse outlier languages into ISO 639-3 language codes.
    language_map = {
        # The French phrase for "without linguistic content"
        "Sans contenu linguistique": "zxx",
        "allemand": "deu",
        "ang": "eng",
        "anglais": "eng",
        "espagnol": "spa",
        "français": "fre",
        "latin": "lat",
        "portugais": "por",
    }
    languages = [language_map[d] if d in language_map else d for d in languages]

    return list(set(languages))


def get_tags(record: Record) -> List[str]:
    tags = []

    types = get_english_attr(record, "dc:type")
    if types is not None:
        tags += types

    # Discard useless tags
    useless_tags = [
        "still image",
        "image",
        "text",
        "view",
    ]
    tags = [d.title() for d in tags if d not in useless_tags]
    return list(set(tags))


def get_abstract(record: Record) -> Union[str, None]:
    description = get_first_element(get_english_attr(record, "dc:description"))

    formats = get_english_attr(record, "dc:format")
    if formats is not None:
        useless_formats = [
            "image/jpeg",
        ]
        formats = [d for d in formats if d not in useless_formats]

    abstract = None
    if description is not None:
        abstract = description
    if formats is not None:
        if abstract is None:
            abstract = ""
        abstract += ". ".join(formats)

    return abstract


def get_rights(record: Record) -> str:
    rights = get_english_attr(record, "dc:rights")
    if rights is None:
        return "unknown"

    rights = list(set(get_english_attr(record, "dc:rights")))
    assert len(rights) == 1, f"Unexpected rights with length != 1: {rights}"

    if rights == "public domain":
        return "public domain"

    if "restricted use" in rights:
        return "restricted use"

    return "unknown"


def get_display_name(page: Page, record: Record) -> Union[str, None]:
    if "legend" in page:
        return page["legend"]
    return get_first_element(get_english_attr(record, "dc:title"))


def get_image_size(record: Record) -> Union[Dict, None]:
    formats = get_english_attr(record, "dc:format")
    if formats is None:
        return None

    for item in formats:
        if " X " not in item and " x " not in item:
            continue

        sentence = item.replace(", ", ".").replace(",", ".")
        if " X " in sentence:
            match = re.search(r"(\d+(\.\d+)?) X (\d+(\.\d+)?)", sentence)
        else:
            match = re.search(r"(\d+(\.\d+)?) x (\d+(\.\d+)?)", sentence)

        if match is None:
            continue

        width = float(match.group(1))
        height = float(match.group(3))
        unit = None
        if " cm" in sentence:
            unit = "cm"
        elif " mm" in sentence:
            unit = "mm"
        image_size = {"width": width, "height": height, "unit": unit, "rawString": item}
        return image_size
    return None


def process(
    entry: MetadataEntry, img_dir: Union[str, None]
) -> List[BaseProcessedMetadataEntry]:
    """
    Postprocess a metadata entry.
    Create a list of metadata entries from the metadata entry.
    If img directory is not provided, do not compute the image attributes.

    Each metadata entry stored in Gallica contains a list of images.
    """

    metadata_entries = []

    record = entry["sourceData"]["record"]
    pages = entry["sourceData"]["pages"]

    is_book = get_is_book(record)

    # The attributes shared by images in the same collection:
    authors = get_authors(record)
    publish_date = get_publish_date(record)
    languages = get_languages(record)
    tags = get_tags(record)
    abstract = get_abstract(record)
    # image_size = get_image_size(record)
    source = {
        "name": entry["source"],
        "url": entry["url"],
        "accessDate": entry["accessDate"],
    }

    for i, page in enumerate(pages):
        # If the collection is a book, its book cover images should be ignored.
        # The first and the last images are usually the book cover images.
        if i in {0, len(pages) - 1} and is_book:
            continue

        # Note: use the UUID of each page instead of
        # the UUID of the entire source data.
        uuid = get_image_uuid(page, entry)
        view_url = get_view_url(page, entry)
        download_url = get_image_url(page, entry)

        image_attributes = (
            {}
            if img_dir is None
            else {
                "md5": get_md5_by_uuid(uuid, img_dir),
                "phash": get_phash_by_uuid(uuid, img_dir),
                "resolution": get_shape_by_uuid(uuid, img_dir),
                "fileSize": get_storage_size_by_uuid(uuid, img_dir),
            }
        )

        metadata_entries.append(
            {
                "uuid": uuid,
                "authors": authors,
                "displayName": get_display_name(page, record),
                "publishDate": publish_date,
                "viewUrl": view_url,
                "downloadUrl": download_url,
                **image_attributes,
                "languages": languages,
                "tags": tags,
                "abstract": abstract,
                "rights": get_rights(record),
                "source": source,
                # 'imageSize': image_size,
            }
        )
    return metadata_entries


def process_batch(
    metadata_path: str, img_dir: Union[str, None]
) -> List[BaseProcessedMetadataEntry]:
    """
    Postprocess a batch of metadata entries.
    """

    metadata = load_jl(metadata_path)
    processed_metadata = []
    for d in tqdm(metadata, desc="Process Metadata Progress"):
        if "pages" not in d["sourceData"]:
            continue
        processed_metadata += process(d, img_dir)

    if img_dir is None:
        return processed_metadata
    # Ignore the entries where the phash computation failed,
    # meaning that the corresponding image has not been fetched
    # or the fetched image is corrupted.
    return [d for d in processed_metadata if d["phash"] is not None]
