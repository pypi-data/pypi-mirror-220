"""
The entrance to querier class.
"""

import json
import os
from typing import Union

from jsonschema import validate
from libquery import LibraryOfCongress as _LibraryOfCongress
from libquery.utils.jsonl import load_jl

from ._process_metadata import process_batch
from ._schema import schema_metadata


def process_metadata(
    metadata_path: str, img_dir: Union[str, None], processed_metadata_path: str
) -> None:
    output_dir = os.path.dirname(processed_metadata_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    metadata = process_batch(metadata_path, img_dir)
    with open(processed_metadata_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(metadata, indent=4, ensure_ascii=False))


class LibraryOfCongress(_LibraryOfCongress):
    """
    The querier for the `Library of Congress` data source.
    """

    def validate_metadata(self) -> None:
        metadata = load_jl(self.metadata_path)
        validate(instance=metadata, schema=schema_metadata)

    def process_metadata(self, path: str) -> None:
        process_metadata(self.metadata_path, self.img_dir, path)

    def process_metadata_fast(self, path: str) -> None:
        process_metadata(self.metadata_path, None, path)
