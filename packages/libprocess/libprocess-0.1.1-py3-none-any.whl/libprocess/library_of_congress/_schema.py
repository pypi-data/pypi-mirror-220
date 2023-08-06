"""
Schema declarations used for validating the data structure of metadata.
"""

schema_item = {
    "type": "object",
    "properties": {
        "created_published": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "digital_id": {"type": "array", "items": {"type": "string"}},
        "format": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "language": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "notes": {"type": "array", "items": {"type": "string"}},
        "repository": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "title": {"type": "string"},
        "date": {"type": "string"},
        "location": {"type": "array", "items": {"type": "string"}},
        "medium": {"type": "array", "items": {"type": "string"}},
        "other_title": {"type": "array", "items": {"type": "string"}},
        "source_collection": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "subjects": {"type": "array", "items": {"type": "string"}},
        "translated_title": {"type": "array", "items": {"type": "string"}},
        "call_number": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "contributors": {"type": "array", "items": {"type": "string"}},
        "number_former_id": {"type": "array", "items": {"type": "string"}},
        "contents": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "creator": {"type": "string"},
        "genre": {"type": "array", "items": {"type": "string"}},
        "summary": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "rights": {"type": "string"},
        "reproduction_number": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "access_advisory": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "related_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"title": {"type": "string"}, "url": {"type": "string"}},
                "required": ["title", "url"],
            },
        },
        "rights_advisory": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "control_number": {"type": "string"},
        "created": {"type": "string"},
        "created_published_date": {"type": "string"},
        "creators": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "link": {"type": "string"},
                    "role": {"type": "string"},
                    "title": {"type": "string"},
                },
                "required": ["link", "role", "title"],
            },
        },
        "display_offsite": {"type": "boolean"},
        "formats": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"link": {"type": "string"}, "title": {"type": "string"}},
                "required": ["link", "title"],
            },
        },
        "id": {"type": "string"},
        "link": {"type": "string"},
        "marc": {"type": "string"},
        "medium_brief": {"type": "string"},
        "mediums": {"type": "array", "items": {"type": "string"}},
        "modified": {"type": "string"},
        "resource_links": {"type": "array", "items": {"type": "string"}},
        "rights_information": {"type": "string"},
        "service_low": {"type": "string"},
        "service_medium": {"type": "string"},
        "sort_date": {"type": "string"},
        "source_created": {"type": "string"},
        "source_modified": {"type": "string"},
        "stmt_of_responsibility": {"type": "string"},
        "subject_headings": {"type": "array", "items": {"type": "string"}},
        "thumb_gallery": {"type": "string"},
    },
    "required": [],
    "additionalProperties": True,
}

schema_resource = {
    "type": "object",
    "properties": {
        "files": {"type": "integer"},
        "image": {"type": "string"},
        "search": {"type": "string"},
        "segments": {"type": "integer"},
        "url": {"type": "string"},
        "caption": {"type": "string"},
        "captions": {"type": ["integer", "string"]},
        "zip": {"type": "string"},
        "pdf": {"type": "string"},
        "representative_index": {"type": "integer"},
        "djvu_text_file": {"type": "string"},
        "fulltext_derivative": {"type": "string"},
        "fulltext_file": {"type": "string"},
        "paprika_resource_path": {"type": "string"},
        "version": {"type": "integer"},
    },
    "required": [],
    "additionalProperties": True,
}

schema_source_data = {
    "type": "object",
    "properties": {
        "access_restricted": {"type": "boolean"},
        "aka": {"type": "array", "items": {"type": "string"}},
        "campaigns": {"type": "array"},
        "date": {"type": "string"},
        "dates": {"type": "array", "items": {"type": "string"}},
        "description": {"type": "array", "items": {"type": "string"}},
        "digitized": {"type": "boolean"},
        "extract_timestamp": {"type": "string"},
        "group": {"type": "array", "items": {"type": "string"}},
        "hassegments": {"type": "boolean"},
        "id": {"type": "string"},
        "image_url": {"type": "array", "items": {"type": "string"}},
        "index": {"type": "integer"},
        "item": schema_item,
        "language": {"type": "array", "items": {"type": "string"}},
        "location": {"type": "array", "items": {"type": "string"}},
        "mime_type": {"type": "array", "items": {"type": "string"}},
        "number": {"type": "array", "items": {"type": "string"}},
        "number_source_modified": {"type": "array", "items": {"type": "string"}},
        "online_format": {"type": "array", "items": {"type": "string"}},
        "original_format": {"type": "array", "items": {"type": "string"}},
        "other_title": {"type": "array", "items": {"type": "string"}},
        "partof": {"type": "array", "items": {"type": "string"}},
        "resources": {
            "type": "array",
            "items": schema_resource,
        },
        "segments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "count": {"type": "integer"},
                    "link": {"type": "string"},
                    "url": {"type": "string"},
                },
                "required": ["count", "link", "url"],
            },
        },
        "shelf_id": {"type": "string"},
        "site": {"type": "array", "items": {"type": "string"}},
        "timestamp": {"type": "string"},
        "title": {"type": "string"},
        "url": {"type": "string"},
        "number_lccn": {"type": "array", "items": {"type": "string"}},
        "number_related_items": {"type": "array", "items": {"type": "string"}},
        "subject": {"type": "array", "items": {"type": "string"}},
        "contributor": {"type": "array", "items": {"type": "string"}},
        "location_country": {"type": "array", "items": {"type": "string"}},
        "location_county": {"type": "array", "items": {"type": "string"}},
        "location_state": {"type": "array", "items": {"type": "string"}},
        "number_former_id": {"type": "array", "items": {"type": "string"}},
        "number_carrier_type": {"type": "array", "items": {"type": "string"}},
        "type": {"type": "array", "items": {"type": "string"}},
        "location_city": {"type": "array", "items": {"type": "string"}},
        "number_oclc": {"type": "array", "items": {"type": "string"}},
        "related": {
            "type": "object",
            "properties": {
                "group_record": {"type": "string"},
                "neighbors": {"type": "string"},
            },
            "required": ["neighbors"],
        },
        "reproductions": {"type": "string"},
        "unrestricted": {"type": "boolean"},
        "publication_frequency": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "access_restricted",
        "aka",
        "campaigns",
        "digitized",
        "extract_timestamp",
        "group",
        "hassegments",
        "id",
        "image_url",
        "index",
        "item",
        "mime_type",
        "online_format",
        "original_format",
        "other_title",
        "partof",
        "resources",
        "shelf_id",
        "timestamp",
        "title",
        "url",
    ],
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
