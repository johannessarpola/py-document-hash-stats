import app.src.models as m
import json


def json_to_document_hash(json):
    id = json["hash"]
    content = json["content"]
    attributes = json["attributes"]
    return m.DocumentHash(id, content, attributes)


def document_hashes_from_jsons(lst):
    document_hashes = []
    for document_hash_json in lst:
        dh = json_to_document_hash(document_hash_json)
        document_hashes.append(dh)
    return document_hashes


def call_if_obj_has_method_or_default(obj, name, default):
    op = getattr(obj, name, None)
    if callable(op):
        return op()
    else:
        return default


def json_format(obj):
    jsonObj = call_if_obj_has_method_or_default(obj, 'as_json', obj)
    return jsonObj


def aggregate_stats_to_json(aggr_stats):
    return json.dumps(json_format(aggr_stats), indent=4, default=lambda o: o.__dict__)
