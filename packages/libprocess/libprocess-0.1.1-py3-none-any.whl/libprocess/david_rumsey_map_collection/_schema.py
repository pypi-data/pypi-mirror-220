"""
Schema declarations used for validating the data structure of metadata.
"""

schema_source_data = {
    "type": "object",
    "properties": {
        "displayName": {"type": "string"},
        "description": {"type": "string"},
        "mediaType": {"type": "string"},
        "fieldValues": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "Author": {"type": "array", "items": {"type": "string"}},
                    "Date": {"type": "array", "items": {"type": "string"}},
                    "Short Title": {"type": "array", "items": {"type": "string"}},
                    "Publisher": {"type": "array", "items": {"type": "string"}},
                    "Publisher Location": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "Type": {"type": "array", "items": {"type": "string"}},
                    "Obj Height cm": {"type": "array", "items": {"type": "string"}},
                    "Obj Width cm": {"type": "array", "items": {"type": "string"}},
                    "Subject": {"type": "array", "items": {"type": "string"}},
                    "Full Title": {"type": "array", "items": {"type": "string"}},
                    "List No": {"type": "array", "items": {"type": "string"}},
                    "Page No": {"type": "array", "items": {"type": "string"}},
                    "Series No": {"type": "array", "items": {"type": "string"}},
                    "Publication Author": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "Pub Date": {"type": "array", "items": {"type": "string"}},
                    "Pub Title": {"type": "array", "items": {"type": "string"}},
                    "Pub Reference": {"type": "array", "items": {"type": "string"}},
                    "Pub Note": {"type": "array", "items": {"type": "string"}},
                    "Pub List No": {"type": "array", "items": {"type": "string"}},
                    "Pub Type": {"type": "array", "items": {"type": "string"}},
                    "Pub Maps": {"type": "array", "items": {"type": "string"}},
                    "Pub Height cm": {"type": "array", "items": {"type": "string"}},
                    "Pub Width cm": {"type": "array", "items": {"type": "string"}},
                    "Image No": {"type": "array", "items": {"type": "string"}},
                    "Download 1": {"type": "array", "items": {"type": "string"}},
                    "Download 2": {"type": "array", "items": {"type": "string"}},
                    "Authors": {"type": "array", "items": {"type": "string"}},
                    "Note": {"type": "array", "items": {"type": "string"}},
                    "Reference": {"type": "array", "items": {"type": "string"}},
                    "World Area": {"type": "array", "items": {"type": "string"}},
                    "Collection": {"type": "array", "items": {"type": "string"}},
                    "Scale 1": {"type": "array", "items": {"type": "string"}},
                    "Country": {"type": "array", "items": {"type": "string"}},
                    "Engraver or Printer": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "Region": {"type": "array", "items": {"type": "string"}},
                    "State/Province": {"type": "array", "items": {"type": "string"}},
                    "City": {"type": "array", "items": {"type": "string"}},
                    "Event": {"type": "array", "items": {"type": "string"}},
                    "County": {"type": "array", "items": {"type": "string"}},
                    "Attributed Author": {"type": "array", "items": {"type": "string"}},
                    "Attributed Publication Author": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
        "relatedFieldValues": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "pub_list_no": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["pub_list_no"],
                "additionalProperties": False,
            },
        },
        "id": {"type": "string"},
        "iiifManifest": {"type": "string"},
        "urlSize0": {"type": "string"},
        "urlSize1": {"type": "string"},
        "urlSize2": {"type": "string"},
        "urlSize3": {"type": "string"},
        "urlSize4": {"type": "string"},
        "refUrlSize0": {"type": "string"},
        "refUrlSize1": {"type": "string"},
        "refUrlSize2": {"type": "string"},
        "refUrlSize3": {"type": "string"},
        "refUrlSize4": {"type": "string"},
    },
    "required": [
        "description",
        "displayName",
        "fieldValues",
        "id",
        "iiifManifest",
        "mediaType",
        "relatedFieldValues",
        "urlSize2",
    ],
    "additionalProperties": False,
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
    "required": ["accessDate", "idInSource", "source", "sourceData", "url", "uuid"],
    "additionalProperties": False,
}

schema_metadata = {"type": "array", "items": schema_metadata_entry}
