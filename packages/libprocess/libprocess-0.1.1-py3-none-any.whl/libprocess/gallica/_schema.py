"""
Schema declarations used for validating the data structure of metadata.

Reference: https://api.bnf.fr/api-gallica-de-recherche
"""

schema_text_with_lang = {
    "type": "object",
    "properties": {"@xml:lang": {"type": "string"}, "#text": {"type": "string"}},
    "required": ["#text", "@xml:lang"],
    "additionalProperties": False,
}

schema_record = {
    "type": "object",
    "properties": {
        "@xmlns:dc": {"type": "string"},
        "@xmlns:oai_dc": {"type": "string"},
        "@xmlns:xsi": {"type": "string"},
        "@xsi:schemaLocation": {"type": "string"},
        "dc:identifier": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "dc:title": {
            "anyOf": [
                {"type": "string"},
                {
                    "type": "array",
                    "items": {"anyOf": [{"type": "string"}, schema_text_with_lang]},
                },
            ]
        },
        # The author(s).
        "dc:creator": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        # The edition's publish date.
        "dc:date": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "dc:subject": {
            "anyOf": [
                {"type": "string"},
                {"type": "null"},
                {
                    "type": "array",
                    "items": {"anyOf": [{"type": "string"}, schema_text_with_lang]},
                },
                schema_text_with_lang,
            ]
        },
        "dc:coverage": {
            "anyOf": [
                {"type": "string"},
                {"type": "null"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "dc:format": {
            "anyOf": [
                {"type": "string"},
                {
                    "type": "array",
                    "items": {"anyOf": [{"type": "string"}, schema_text_with_lang]},
                },
                schema_text_with_lang,
            ]
        },
        # For collections within the BnF, the language code has 3 characters.
        # For collections from outside, the language code can be arbitrary.
        "dc:language": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "dc:relation": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        # Type of the document, e.g., monograph, map, image,
        # fascicle, manuscript, score, sound, object and video.
        "dc:type": {
            "type": "array",
            "items": {"anyOf": [{"type": "string"}, schema_text_with_lang]},
        },
        "dc:source": {"type": "string"},
        "dc:rights": {"type": "array", "items": schema_text_with_lang},
        "dc:publisher": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "dc:description": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "dc:contributor": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "#text": {"type": "string"},
    },
    "required": [
        "@xmlns:dc",
        "@xmlns:oai_dc",
        "@xmlns:xsi",
        "@xsi:schemaLocation",
        "dc:identifier",
        "dc:relation",
        "dc:source",
        "dc:title",
    ],
    "additionalProperties": False,
}

schema_page = {
    "type": "object",
    "properties": {
        "numero": {"type": ["null", "string"]},
        "ordre": {"type": "string"},
        "pagination_type": {"type": ["null", "string"]},
        "image_width": {"type": "string"},
        "image_height": {"type": "string"},
        "legend": {"type": "string"},
    },
    "required": ["image_height", "image_width", "numero", "ordre", "pagination_type"],
    "additionalProperties": False,
}

schema_source_data = {
    "type": "object",
    "properties": {
        "identifier": {"type": "string"},
        "record": schema_record,
        "pages": {"type": "array", "items": schema_page},
    },
    "required": ["identifier"],
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
    "required": ["uuid", "url", "source", "idInSource", "accessDate", "sourceData"],
    "additionalProperties": False,
}

schema_metadata = {"type": "array", "items": schema_metadata_entry}
