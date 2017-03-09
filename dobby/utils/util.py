"""Helper functions.
"""
import json
__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])

def get_float_value(json_dict, key):
    try:
        value = float(json_dict[key]) if json_dict.get(key, None) else None
    except ValueError:
        print ("Cannot convert to float", json_dict.get(key, None))
        return None
    else:
        return value


def read_json(filename):
    json_to_return = None
    try:
        with open(fname) as f:
            json_to_return = json.load(f)
    except (OSError, IOError) as e:
        raise IllegalArgumentError("Cannot read file", filename)
        return None
    else:
        return json_to_return
