# -*- coding: utf-8 -*-

import gzip
import json

def make_json_response(data, status=None):
    status = 200 if status is None else status
    data["http_status"] = status
    return data

def compress_JSON(data):
    # Convert serializable data to JSON string
    json_data = json.dumps(data, indent=2)
    # Convert JSON string to bytes
    encoded = json_data.encode("utf-8")
    # Compress
    compressed = gzip.compress(encoded)
    return compressed