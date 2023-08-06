"""
Schema declarations used for validating the data structure of metadata.
"""

schema_file = {
    "type": "object",
    "required": ["name", "source", "format", "md5"],
    "properties": {
        "name": {"type": "string"},
        "source": {"type": "string"},
        "format": {"type": "string"},
        "md5": {"type": "string"},
        "btih": {"type": "string"},
        "mtime": {"type": "string"},
        "size": {"type": "string"},
        "crc32": {"type": "string"},
        "sha1": {"type": "string"},
        "rotation": {"type": "string"},
        "original": {"type": "string"},
    },
    "additionalProperties": True,
}

schema_internet_archive_metadata = {
    "type": "object",
    "required": [
        "identifier",
        "collection",
        "mediatype",
        "title",
        "uploader",
        "publicdate",
        "addeddate",
    ],
    "properties": {
        "identifier": {"type": "string"},
        "collection": {
            "anyOf": [
                {"type": "array", "items": {"type": "string"}},
                {"type": "string"},
            ]
        },
        "description": {
            "anyOf": [
                {"type": "array", "items": {"type": "string"}},
                {"type": "string"},
            ]
        },
        "mediatype": {"type": "string"},
        "title": {"type": "string"},
        "uploader": {"type": "string"},
        "publicdate": {"type": "string"},
        "addeddate": {"type": "string"},
        "call_number": {"type": "string"},
        "coverage": {
            "anyOf": [
                {"type": "array", "items": {"type": "string"}},
                {"type": "string"},
            ]
        },
        "creator": {
            "anyOf": [
                {"type": "array", "items": {"type": "string"}},
                {"type": "string"},
            ]
        },
        "date": {
            "anyOf": [
                {"type": "array", "items": {"type": "string"}},
                {"type": "string"},
            ]
        },
        "external-identifier": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "format": {"type": "string"},
        "language": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "map-type": {
            "anyOf": [
                {"type": "array", "items": {"type": "string"}},
                {"type": "string"},
            ]
        },
        "publisher": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "rights": {"type": "string"},
        "scanner": {"type": "string"},
        "size": {"type": "string"},
        "source": {"type": "string"},
        "subject": {
            "anyOf": [
                {"type": "array", "items": {"type": "string"}},
                {"type": "string"},
            ]
        },
        "warning": {"type": "string"},
        "year": {"type": "string"},
        "isbn": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "issn": {"type": "string"},
        "date_range": {"type": "string"},
    },
    "additionalProperties": True,
}

schema_page = {
    "type": "object",
    "required": ["confidence", "leafNum", "ocr_value", "pageNumber"],
    "properties": {
        "confidence": {"type": "number"},
        "leafNum": {"type": "integer"},
        "ocr_value": {"type": "array", "items": {"type": "string"}},
        "pageNumber": {"type": "string"},
    },
    "additionalProperties": False,
}

schema_page_numbers = {
    "type": "object",
    "required": [
        "confidence",
        "pages",
        "identifier",
    ],
    "properties": {
        "confidence": {"type": "number"},
        "pages": {"type": "array", "items": schema_page},
        "identifier": {"type": "string"},
    },
    "additionalProperties": False,
}

schema_source_data = {
    "type": "object",
    "required": [
        "created",
        "d1",
        "d2",
        "dir",
        "files",
        "files_count",
        "item_last_updated",
        "item_size",
        "metadata",
        "server",
        "uniq",
        "workable_servers",
    ],
    "properties": {
        "created": {"type": "integer"},
        "d1": {"type": "string"},
        "d2": {"type": "string"},
        "dir": {"type": "string"},
        "events": {"type": "object"},
        "files": {"type": "array", "items": schema_file},
        "files_count": {"type": "integer"},
        "item_last_updated": {"type": "integer"},
        "item_size": {"type": "integer"},
        "metadata": schema_internet_archive_metadata,
        "page_numbers": schema_page_numbers,
        "server": {"type": "string"},
        "uniq": {"type": "integer"},
        "workable_servers": {"type": "array", "items": {"type": "string"}},
        "reviews": {"type": "array", "items": {"type": "string"}},
        "servers_unavailable": {"type": "boolean"},
    },
    "additionalProperties": True,
}

schema_metadata_entry = {
    "type": "object",
    "properties": {
        "uuid": {"type": "string"},
        "url": {"type": "string"},
        "source": {"type": "string"},
        "idInSource": {"type": "string"},
        "accessDate": {"type": "string"},
        "sourceData": schema_source_data,
    },
    "required": ["uuid", "url", "source", "idInSource", "accessDate", "sourceData"],
    "additionalProperties": False,
}

schema_metadata = {"type": "array", "items": schema_metadata_entry}
