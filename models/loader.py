import json

import numpy as np
import pandas as pd

from flatten_json import flatten


def load_json_lines(filename):
    list = []
    with open(filename) as file:
        for line in file:
            print(f"line = {line}")
            list.append(json.loads(line))
    return list


def load_json(filename):
    with open(filename) as file:
        result = json.load(file)
    return result


def flat_json(input):
    """
    Function using the recursive flattener:
    https://github.com/amirziai/flatten

    :param: a list of (nested) dictionaries or a (nested) dictionary
    :return: a dataframe
    """
    result = None
    if isinstance(input, list):
        print("input is a list")
        flattened = [flatten(element) for element in input]
        result = pd.DataFrame(flattened)
    else:
        print(f"input is a dictionary : {type(input)}")
        flattened = flatten(input)
        result = pd.DataFrame([flattened])
    return result
