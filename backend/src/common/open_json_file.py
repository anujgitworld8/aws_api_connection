import json


def with_open_read_json_file(fileName):
    properties = None
    with open(fileName, "r") as fp:
        properties = json.load(fp)
    return properties
